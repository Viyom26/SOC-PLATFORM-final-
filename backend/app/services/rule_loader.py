from app.models.detection_rule import DetectionRule
import uuid

def load_default_rules(db):

    count = db.query(DetectionRule).count()
    print("🔍 Rule Loader - Existing count:", count)

    if count > 0:
        print("⚠️ Rules already exist, skipping insert")
        return

    rules = [
        DetectionRule(
            id=str(uuid.uuid4()),
            name="Multiple Failed Logins",
            description="Detect brute force attempts",
            pattern="failed login",
            threshold=5,
            severity="HIGH",
            enabled=True
        ),
        DetectionRule(
            id=str(uuid.uuid4()),
            name="Port Scan Detection",
            description="Detect scanning activity",
            pattern="scan",
            threshold=10,
            severity="MEDIUM",
            enabled=True
        ),
        DetectionRule(
            id=str(uuid.uuid4()),
            name="Suspicious IP Activity",
            description="Detect malicious IP behavior",
            pattern="malicious",
            threshold=1,
            severity="CRITICAL",
            enabled=True
        ),
    ]

    db.add_all(rules)
    db.commit()

    print("✅ Default detection rules inserted")