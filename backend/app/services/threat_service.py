from collections import defaultdict

def aggregate_attacks(logs):

    data = defaultdict(lambda: {
        "attack_count":0
    })

    for log in logs:

        key = f"{log.src_ip}->{log.dst_ip}"

        data[key]["src_ip"] = log.src_ip
        data[key]["dst_ip"] = log.dst_ip

        data[key]["attack_count"] += 1

    return list(data.values())