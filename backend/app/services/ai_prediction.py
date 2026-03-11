def predict_future_risk(current_risk: float) -> float:
    """
    Simple projection logic for future risk.
    Can be replaced later with ML models.
    """

    if current_risk is None:
        return 0

    return min(100, current_risk * 1.1)