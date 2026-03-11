import ipaddress

def calculate_ip_score(ip: str) -> int:
    """
    Heuristic IP risk score (0–100)
    This is NOT VirusTotal.
    This is logic-based SOC scoring.
    """

    try:
        ip_obj = ipaddress.ip_address(ip)

        # 🟢 Private / internal IPs (SAFE)
        if ip_obj.is_private:
            return 5

        # 🟢 Loopback
        if ip_obj.is_loopback:
            return 1

        # 🟡 Reserved / special ranges
        if ip_obj.is_reserved or ip_obj.is_multicast:
            return 20

        # 🟡 Known public DNS (low risk)
        known_safe = {
            "8.8.8.8", "8.8.4.4",       # Google
            "1.1.1.1", "1.0.0.1",       # Cloudflare
            "9.9.9.9",                  # Quad9
        }
        if ip in known_safe:
            return 15

        # 🔴 TOR exit node ranges (heuristic examples)
        tor_prefixes = (
            "185.220.",  # TOR
            "185.129.",
            "176.10."
        )
        if ip.startswith(tor_prefixes):
            return 90

        # 🔴 Hosting / VPS ranges (often abused)
        hosting_prefixes = (
            "45.", "46.", "89.", "91.", "95.", "103.", "104."
        )
        if ip.startswith(hosting_prefixes):
            return 70

        # 🟠 Unknown public IP (medium risk)
        return 50

    except ValueError:
        # Invalid IP format
        return 0
