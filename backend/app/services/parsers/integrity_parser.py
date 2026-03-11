def parse_integrity_row(row):
    
    return {
        "source_ip": "host",
        "destination_ip": "file-system",
        "source_port": "0",
        "destination_port": "0",
        "protocol": "FILE",
        "severity": "MEDIUM",
        "message": str(row[2]) if len(row) > 2 else "File Change",
    }