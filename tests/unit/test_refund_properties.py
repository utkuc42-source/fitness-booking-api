from datetime import datetime, timedelta

from hypothesis import given, strategies as st

from app.domain.refund import RefundPolicy


@given(
    paid_price=st.floats(min_value=0, max_value=10_000),
    hours_before_start=st.integers(min_value=0, max_value=72),
)
def test_refund_is_never_negative_and_never_more_than_paid(
    paid_price: float,
    hours_before_start: int,
):
    policy = RefundPolicy()

    class_start = datetime(2025, 12, 31, 12, 0)
    cancelled_at = class_start - timedelta(hours=hours_before_start)

    result = policy.calculate_refund(
        paid_price=paid_price,
        class_start=class_start,
        cancelled_at=cancelled_at,
    )

    assert 0.0 <= result.refund_amount <= paid_price
