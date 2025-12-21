from datetime import datetime

import pytest

from app.domain.pricing import MembershipType, PricingService


# Decision table derived tests (base_price = 100)
# Peak: 19:00, Off-peak: 10:00
# Surge: occupancy_rate > 0.80 (use 0.90), No surge: use 0.50
@pytest.mark.parametrize(
    "membership,is_peak,is_surge,expected",
    [
        # standard
        (MembershipType.standard, False, False, 100.00),
        (MembershipType.standard, False, True, 130.00),
        (MembershipType.standard, True, False, 120.00),
        (MembershipType.standard, True, True, 156.00),
        # student
        (MembershipType.student, False, False, 85.00),
        (MembershipType.student, False, True, 110.50),
        (MembershipType.student, True, False, 102.00),
        (MembershipType.student, True, True, 132.60),
        # premium
        (MembershipType.premium, False, False, 75.00),
        (MembershipType.premium, False, True, 97.50),
        (MembershipType.premium, True, False, 90.00),
        (MembershipType.premium, True, True, 117.00),
    ],
)
def test_pricing_from_decision_table(membership, is_peak, is_surge, expected):
    svc = PricingService()

    start = datetime(2025, 12, 20, 19, 0) if is_peak else datetime(2025, 12, 20, 10, 0)
    occupancy_rate = 0.90 if is_surge else 0.50

    res = svc.calculate(
        base_price=100.0,
        membership=membership,
        class_start=start,
        occupancy_rate=occupancy_rate,
    )

    assert res.final_price == expected

def test_peak_boundary_18_00_is_peak():
    svc = PricingService()
    res = svc.calculate(
        base_price=100.0,
        membership=MembershipType.standard,
        class_start=datetime(2025, 12, 20, 18, 0),
        occupancy_rate=0.0,
    )
    assert res.peak_factor == 1.20


def test_peak_boundary_22_00_is_offpeak():
    svc = PricingService()
    res = svc.calculate(
        base_price=100.0,
        membership=MembershipType.standard,
        class_start=datetime(2025, 12, 20, 22, 0),
        occupancy_rate=0.0,
    )
    assert res.peak_factor == 1.00
