# Country risk weights (can later move to DB)

COUNTRY_RISK_WEIGHTS = {
    "Russia": 25,
    "China": 20,
    "North Korea": 30,
    "Iran": 20,
    "Belarus": 15,
    "Syria": 15,
}

def get_country_risk(country: str) -> int:
    if not country:
        return 0

    return COUNTRY_RISK_WEIGHTS.get(country, 0)
