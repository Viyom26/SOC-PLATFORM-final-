import requests

def get_country(ip: str):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        return res.json().get("country", "Unknown")
    except:
        return "Unknown"
