from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.domain.pricing import MembershipType, PricingService
from app.domain.refund import RefundPolicy
from app.domain.reservation_rules import assert_capacity_not_exceeded

from datetime import datetime, timezone


app = FastAPI(title="Fitness Booking API")

pricing_service = PricingService()
refund_policy = RefundPolicy()

# ---------- In-memory stores ----------
members: Dict[int, dict] = {}
classes: Dict[int, dict] = {}
reservations: Dict[int, dict] = {}

member_seq = 1
class_seq = 1
reservation_seq = 1


def reset_in_memory():
    """Used by integration tests to ensure clean state between tests."""
    global member_seq, class_seq, reservation_seq
    members.clear()
    classes.clear()
    reservations.clear()
    member_seq = 1
    class_seq = 1
    reservation_seq = 1


# ---------- API schemas ----------
class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    membership: MembershipType


class ClassCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    instructor: str = Field(min_length=1, max_length=100)
    capacity: int = Field(gt=0, le=200)
    starts_at: datetime
    base_price: float = Field(ge=0, le=10_000)


class ReservationCreate(BaseModel):
    member_id: int
    class_id: int


# ---------- Health ----------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- Members ----------
@app.post("/members")
def add_member(payload: MemberCreate):
    global member_seq
    m = {
        "id": member_seq,
        "name": payload.name,
        "membership": payload.membership,  # store Enum
    }
    members[member_seq] = m
    member_seq += 1
    return m


@app.get("/members/{member_id}")
def get_member(member_id: int):
    m = members.get(member_id)
    if not m:
        raise HTTPException(status_code=404, detail="member not found")
    return m


# ---------- Classes ----------
@app.post("/classes")
def create_class(payload: ClassCreate):
    global class_seq
    c = {
        "id": class_seq,
        "name": payload.name,
        "instructor": payload.instructor,
        "capacity": payload.capacity,
        "starts_at": payload.starts_at,
        "base_price": payload.base_price,
    }
    classes[class_seq] = c
    class_seq += 1
    return c


@app.get("/classes")
def list_classes() -> List[dict]:
    return list(classes.values())


# ---------- Reservations ----------
@app.post("/reservations")
def reserve(payload: ReservationCreate):
    global reservation_seq

    m = members.get(payload.member_id)
    if not m:
        raise HTTPException(status_code=404, detail="member not found")

    c = classes.get(payload.class_id)
    if not c:
        raise HTTPException(status_code=404, detail="class not found")

    # Count active reservations for that class
    reserved_count = sum(
        1
        for r in reservations.values()
        if (r["class_id"] == c["id"] and not r["is_cancelled"])
    )

    # Capacity invariant
    try:
        assert_capacity_not_exceeded(capacity=c["capacity"], current_reserved=reserved_count)
    except OverflowError:
        raise HTTPException(status_code=409, detail="class capacity full")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    occupancy_rate = reserved_count / c["capacity"]

    # Dynamic price
    try:
        price = pricing_service.calculate(
            base_price=c["base_price"],
            membership=m["membership"],
            class_start=c["starts_at"],
            occupancy_rate=occupancy_rate,
        ).final_price
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    r = {
        "id": reservation_seq,
        "member_id": m["id"],
        "class_id": c["id"],
        "created_at": datetime.now(timezone.utc),
        "paid_price": price,
        "is_cancelled": False,
        "cancelled_at": None,
        "refund_amount": 0.0,
        "occupancy_rate_before": occupancy_rate,
    }
    reservations[reservation_seq] = r
    reservation_seq += 1
    return r


@app.delete("/reservations/{reservation_id}")
def cancel(reservation_id: int):
    r = reservations.get(reservation_id)
    if not r:
        raise HTTPException(status_code=404, detail="reservation not found")
    if r["is_cancelled"]:
        raise HTTPException(status_code=409, detail="reservation already cancelled")

    c = classes.get(r["class_id"])
    if not c:
        raise HTTPException(status_code=500, detail="class data missing for reservation")

    cancelled_at = datetime.now(timezone.utc)

    try:
        refund_res = refund_policy.calculate_refund(
            paid_price=r["paid_price"],
            class_start=c["starts_at"],
            cancelled_at=cancelled_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    r["is_cancelled"] = True
    r["cancelled_at"] = cancelled_at
    r["refund_amount"] = refund_res.refund_amount
    return r
