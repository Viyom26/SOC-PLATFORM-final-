import random

def get_ip_reputation(ip: str) -> int:
    """
    Simulated IP reputation engine.
    Later we can connect to VirusTotal / AbuseIPDB.
    """

    # Example logic (demo intelligence layer)
    if ip.startswith("185.") or ip.startswith("45."):
        return 80  # Known malicious ASN ranges

    if ip.startswith("8.8.8.") or ip.startswith("1.1.1."):
        return 5  # Trusted public DNS

    # Default random reputation
    return random.randint(10, 60)
