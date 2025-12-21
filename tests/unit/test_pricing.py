from datetime import datetime

import pytest

from app.domain.pricing import MembershipType, PricingService


def test_student_offpeak_no_surge():
    svc = PricingService()
    start = datetime(2025, 12, 20, 10, 0)  # off-peak

    res = svc.calculate(
        base_price=100.0,
        membership=MembershipType.student,
        class_start=start,
        occupancy_rate=0.50,
    )

    assert res.final_price == 85.0  # 100 * 0.85


def test_standard_peak_and_surge():
    svc = PricingService()
    start = datetime(2025, 12, 20, 19, 0)  # peak

    res = svc.calculate(
        base_price=100.0,
        membership=MembershipType.standard,
        class_start=start,
        occupancy_rate=0.90,  # surge
    )

    assert res.final_price == 156.0  # 100 * 1.00 * 1.20 * 1.30


@pytest.mark.parametrize("occ", [-0.1, 1.1])
def test_invalid_occupancy_rejected(occ: float):
    svc = PricingService()
    start = datetime(2025, 12, 20, 10, 0)

    with pytest.raises(ValueError):
        svc.calculate(
            base_price=100.0,
            membership=MembershipType.standard,
            class_start=start,
            occupancy_rate=occ,
        )
