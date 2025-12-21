from __future__ import annotations


def assert_capacity_not_exceeded(*, capacity: int, current_reserved: int) -> None:
    if capacity <= 0:
        raise ValueError("capacity must be > 0")
    if current_reserved < 0:
        raise ValueError("current_reserved must be >= 0")
    if current_reserved >= capacity:
        raise OverflowError("class capacity is full")
