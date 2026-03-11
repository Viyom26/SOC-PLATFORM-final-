from datetime import datetime, timezone
from typing import Union


def apply_risk_decay(score: Union[int, float], analyzed_at) -> float:
    """
    Time-based risk decay engine.
    - Prevents permanent high-risk IPs
    - Handles timezone-naive and timezone-aware datetimes safely
    """

    if not analyzed_at:
        return float(score)

    # Always use UTC now
    now = datetime.now(timezone.utc)

    # 🔥 Fix: Normalize analyzed_at timezone
    if analyzed_at.tzinfo is None:
        analyzed_at = analyzed_at.replace(tzinfo=timezone.utc)

    # Calculate hours difference
    hours_passed = (now - analyzed_at).total_seconds() / 3600

    # 2 points per hour decay
    decay_rate = 2
    decay_value = hours_passed * decay_rate

    new_score = float(score) - decay_value

    # Never go below zero
    return max(round(new_score, 2), 0)
