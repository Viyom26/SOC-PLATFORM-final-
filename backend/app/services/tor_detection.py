import requests

TOR_EXIT_LIST_URL = "https://check.torproject.org/torbulkexitlist"

def is_tor_exit_node(ip: str) -> bool:
    """
    Checks if IP is in Tor exit node list.
    """

    try:
        response = requests.get(TOR_EXIT_LIST_URL, timeout=5)
        if response.status_code != 200:
            return False

        tor_ips = response.text.splitlines()
        return ip in tor_ips

    except Exception:
        return False
