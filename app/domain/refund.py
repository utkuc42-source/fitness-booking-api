from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class RefundResult:
    refund_amount: float
    refund_ratio: float


class RefundPolicy:
    """
    Refund rules based on time-to-start:
    - >= 24 hours: 90%
    - >= 2 hours and < 24 hours: 50%
    - < 2 hours: 0%
    - If cancelled after start time: 0%
    """

    def calculate_refund(
        self,
        *,
        paid_price: float,
        class_start: datetime,
        cancelled_at: datetime,
    ) -> RefundResult:
        if paid_price < 0:
            raise ValueError("paid_price must be >= 0")

        # cancellation after class has started -> no refund
        if cancelled_at > class_start:
            return RefundResult(refund_amount=0.0, refund_ratio=0.0)

        delta = class_start - cancelled_at

        if delta >= timedelta(hours=24):
            ratio = 0.90
        elif delta >= timedelta(hours=2):
            ratio = 0.50
        else:
            ratio = 0.0

        refund = round(paid_price * ratio, 2)
        return RefundResult(refund_amount=refund, refund_ratio=ratio)
