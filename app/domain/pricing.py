from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from enum import Enum


class MembershipType(str, Enum):
    standard = "standard"
    premium = "premium"
    student = "student"


@dataclass(frozen=True)
class PriceBreakdown:
    base_price: float
    membership_factor: float
    peak_factor: float
    surge_factor: float
    final_price: float


class PricingService:
    """
    Rules:
    - Membership factors:
        standard: 1.00
        student:  0.85
        premium:  0.75
    - Peak hours: 18:00-22:00 => 1.20 else 1.00
    - Surge pricing: occupancy_rate > 0.80 => 1.30 else 1.00
    """

    MEMBERSHIP_FACTORS = {
        MembershipType.standard: 1.00,
        MembershipType.student: 0.85,
        MembershipType.premium: 0.75,
    }

    def calculate(
        self,
        *,
        base_price: float,
        membership: MembershipType,
        class_start: datetime,
        occupancy_rate: float,
    ) -> PriceBreakdown:
        if base_price < 0:
            raise ValueError("base_price must be >= 0")
        if not (0.0 <= occupancy_rate <= 1.0):
            raise ValueError("occupancy_rate must be between 0 and 1")

        membership_factor = self.MEMBERSHIP_FACTORS[membership]

        is_peak = time(18, 0) <= class_start.time() < time(22, 0)
        peak_factor = 1.20 if is_peak else 1.00

        surge_factor = 1.30 if occupancy_rate > 0.80 else 1.00

        final = base_price * membership_factor * peak_factor * surge_factor
        final = round(final, 2)

        return PriceBreakdown(
            base_price=base_price,
            membership_factor=membership_factor,
            peak_factor=peak_factor,
            surge_factor=surge_factor,
            final_price=final,
        )
