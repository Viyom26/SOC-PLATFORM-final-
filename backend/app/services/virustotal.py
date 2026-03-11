import os
import requests
from typing import Dict, Any

VT_API_KEY = os.getenv("VT_API_KEY")

VT_EMPTY_RESULT: Dict[str, Any] = {
    "malicious": 0,
    "suspicious": 0,
    "harmless": 0,
    "undetected": 0,
    "timeout": 0,
    "reputation": 0,
    "asn": None,
    "network": None,
    "country": None,
    "tags": [],
    "last_analysis_date": None,
    "total_votes": {
        "harmless": 0,
        "malicious": 0,
    },
    "whois": None,
}


def virustotal_ip_report(ip: str) -> Dict[str, Any]:
    """
    Fetch VirusTotal IP report safely.
    Always returns a valid structure.
    Never breaks main analysis engine.
    """

    # ✅ If API key missing → return safe default
    if not VT_API_KEY:
        return VT_EMPTY_RESULT.copy()

    try:
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        headers = {
            "x-apikey": VT_API_KEY,
            "accept": "application/json",
        }

        response = requests.get(url, headers=headers, timeout=8)

        # ✅ Handle rate limit
        if response.status_code == 429:
            print(f"[VT] Rate limit exceeded for {ip}")
            return VT_EMPTY_RESULT.copy()

        # ✅ Handle invalid API key
        if response.status_code == 401:
            print("[VT] Invalid API key")
            return VT_EMPTY_RESULT.copy()

        if response.status_code != 200:
            print(f"[VT] HTTP {response.status_code} for IP {ip}")
            return VT_EMPTY_RESULT.copy()

        data = response.json().get("data", {})
        attrs = data.get("attributes", {})

        stats = attrs.get("last_analysis_stats", {})

        return {
            "malicious": int(stats.get("malicious", 0)),
            "suspicious": int(stats.get("suspicious", 0)),
            "harmless": int(stats.get("harmless", 0)),
            "undetected": int(stats.get("undetected", 0)),
            "timeout": int(stats.get("timeout", 0)),
            "reputation": int(attrs.get("reputation", 0)),
            "asn": attrs.get("asn"),
            "network": attrs.get("network"),
            "country": attrs.get("country"),
            "tags": attrs.get("tags", []),
            "last_analysis_date": attrs.get("last_analysis_date"),
            "total_votes": attrs.get("total_votes", {
                "harmless": 0,
                "malicious": 0,
            }),
            "whois": attrs.get("whois"),
        }

    except requests.exceptions.Timeout:
        print(f"[VT] Timeout for IP {ip}")
        return VT_EMPTY_RESULT.copy()

    except Exception as e:
        print(f"[VT] Error for IP {ip}: {e}")
        return VT_EMPTY_RESULT.copy()