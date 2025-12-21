from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app, reset_in_memory

from datetime import datetime, timedelta, timezone


@pytest.fixture(autouse=True)
def _reset_state():
    reset_in_memory()


def test_full_happy_path_member_class_reserve_cancel_refund():
    client = TestClient(app)

    # 1) create member
    r = client.post("/members", json={"name": "Utku", "membership": "student"})
    assert r.status_code == 200
    member_id = r.json()["id"]

    # 2) create class (tomorrow -> refund should be 90% if cancelled now)
    starts_at = (datetime.now(timezone.utc) + timedelta(hours=30)).replace(microsecond=0).isoformat()
    r = client.post(
        "/classes",
        json={
            "name": "Yoga",
            "instructor": "Ayse",
            "capacity": 2,
            "starts_at": starts_at,
            "base_price": 100,
        },
    )
    assert r.status_code == 200
    class_id = r.json()["id"]

    # 3) reserve
    r = client.post("/reservations", json={"member_id": member_id, "class_id": class_id})
    assert r.status_code == 200
    reservation_id = r.json()["id"]
    paid_price = r.json()["paid_price"]
    assert paid_price > 0

    # 4) cancel -> should include refund_amount (>=0 and <= paid_price)
    r = client.delete(f"/reservations/{reservation_id}")
    assert r.status_code == 200
    body = r.json()
    assert body["is_cancelled"] is True
    assert 0.0 <= body["refund_amount"] <= paid_price


def test_capacity_full_returns_409():
    client = TestClient(app)

    # member
    r = client.post("/members", json={"name": "A", "membership": "standard"})
    member_id = r.json()["id"]

    # class capacity=1
    starts_at = (datetime.now(timezone.utc) + timedelta(days=1)).replace(microsecond=0).isoformat()
    r = client.post(
        "/classes",
        json={
            "name": "Pilates",
            "instructor": "B",
            "capacity": 1,
            "starts_at": starts_at,
            "base_price": 100,
        },
    )
    class_id = r.json()["id"]

    # first reservation ok
    r = client.post("/reservations", json={"member_id": member_id, "class_id": class_id})
    assert r.status_code == 200

    # second reservation -> 409
    r = client.post("/reservations", json={"member_id": member_id, "class_id": class_id})
    assert r.status_code == 409
    assert r.json()["detail"] == "class capacity full"


def test_unknown_member_or_class_returns_404():
    client = TestClient(app)

    # unknown member
    r = client.post("/reservations", json={"member_id": 999, "class_id": 1})
    assert r.status_code == 404

    # create member
    r = client.post("/members", json={"name": "Utku", "membership": "student"})
    member_id = r.json()["id"]

    # unknown class
    r = client.post("/reservations", json={"member_id": member_id, "class_id": 999})
    assert r.status_code == 404
