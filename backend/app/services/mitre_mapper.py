def map_mitre(severity: str, description: str):
    desc = description.lower()

    if "brute force" in desc:
        return {
            "tactic": "Credential Access",
            "technique_id": "T1110"
        }

    if "powershell" in desc:
        return {
            "tactic": "Execution",
            "technique_id": "T1059"
        }

    if "command and control" in desc:
        return {
            "tactic": "Command and Control",
            "technique_id": "T1071"
        }

    return {
        "tactic": "Unknown",
        "technique_id": "N/A"
    }