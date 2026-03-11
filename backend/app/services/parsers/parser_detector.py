def detect_log_type(headers, first_row_text):
    text = (first_row_text or "").lower()

    header_line = " ".join(headers).lower()

    if "trend micro" in text or "detection type" in header_line:
        return "trendmicro"

    if "eventid" in header_line or "windows" in text:
        return "windows"

    if "firewall" in text or "action" in header_line:
        return "firewall"

    if "file path" in header_line or "integrity" in text:
        return "integrity"

    if "syslog" in text:
        return "syslog"

    return "generic"