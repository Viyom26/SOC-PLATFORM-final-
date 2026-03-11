def parse_trendmicro_row(row):
    
    return {
        "source_ip": row[5] if len(row) > 5 else "Unknown",
        "destination_ip": row[6] if len(row) > 6 else "Unknown",
        "source_port": row[16] if len(row) > 16 else "0",
        "destination_port": row[13] if len(row) > 13 else "0",
        "protocol": row[7] if len(row) > 7 else "Unknown",
        "severity": row[1] if len(row) > 1 else "INFO",
        "message": row[4] if len(row) > 4 else "Unknown",
    }