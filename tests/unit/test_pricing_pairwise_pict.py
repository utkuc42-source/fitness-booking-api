from datetime import datetime

import pytest

from app.domain.pricing import MembershipType, PricingService


def _to_start(timeslot: str) -> datetime:
    return datetime(2025, 12, 20, 19, 0) if timeslot == "peak" else datetime(2025, 12, 20, 10, 0)


def _to_occupancy(occ: str) -> float:
    return 0.90 if occ == "high" else 0.50


@pytest.mark.parametrize(
    "membership,timeslot,occupancy",
    [
        # These should match (a subset of) PICT output rows
        ("standard", "offpeak", "low"),
        ("standard", "peak", "high"),
        ("student", "offpeak", "high"),
        ("student", "peak", "low"),
        ("premium", "offpeak", "low"),
        ("premium", "peak", "high"),
        ("standard", "peak", "low"),
        ("student", "offpeak", "low"),
        ("premium", "offpeak", "high"),
        ("premium", "peak", "low"),
    ],
)
def test_pricing_pairwise_set_from_pict(membership: str, timeslot: str, occupancy: str):
    svc = PricingService()

    res = svc.calculate(
        base_price=100.0,
        membership=MembershipType(membership),
        class_start=_to_start(timeslot),
        occupancy_rate=_to_occupancy(occupancy),
    )

    # Pairwise tests often check "properties" rather than exact numbers.
    # Here we ensure price is within sane bounds for our known multipliers.
    assert 0 <= res.final_price <= 100.0 * 1.30 * 1.20  # max surge+peak+standard

    # And price must be exactly base_price * factors (PricingService guarantees breakdown)
    assert res.final_price == round(
        100.0 * res.membership_factor * res.peak_factor * res.surge_factor, 2
    )
