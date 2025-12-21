from datetime import datetime, timedelta

import pytest

from app.domain.refund import RefundPolicy


def test_refund_24h_or_more_is_90_percent():
    policy = RefundPolicy()
    start = datetime(2025, 12, 21, 10, 0)
    cancelled = start - timedelta(hours=24)

    res = policy.calculate_refund(paid_price=200.0, class_start=start, cancelled_at=cancelled)

    assert res.refund_ratio == 0.90
    assert res.refund_amount == 180.0


def test_refund_between_2h_and_24h_is_50_percent():
    policy = RefundPolicy()
    start = datetime(2025, 12, 21, 10, 0)
    cancelled = start - timedelta(hours=3)

    res = policy.calculate_refund(paid_price=200.0, class_start=start, cancelled_at=cancelled)

    assert res.refund_ratio == 0.50
    assert res.refund_amount == 100.0


def test_refund_less_than_2h_is_zero():
    policy = RefundPolicy()
    start = datetime(2025, 12, 21, 10, 0)
    cancelled = start - timedelta(minutes=30)

    res = policy.calculate_refund(paid_price=200.0, class_start=start, cancelled_at=cancelled)

    assert res.refund_ratio == 0.0
    assert res.refund_amount == 0.0


def test_cancel_after_start_is_zero_refund():
    policy = RefundPolicy()
    start = datetime(2025, 12, 21, 10, 0)
    cancelled = start + timedelta(minutes=1)

    res = policy.calculate_refund(paid_price=200.0, class_start=start, cancelled_at=cancelled)

    assert res.refund_ratio == 0.0
    assert res.refund_amount == 0.0


def test_negative_paid_price_rejected():
    policy = RefundPolicy()
    start = datetime(2025, 12, 21, 10, 0)
    cancelled = start - timedelta(hours=30)

    with pytest.raises(ValueError):
        policy.calculate_refund(paid_price=-1.0, class_start=start, cancelled_at=cancelled)
