import os

# ✅ Read directly from environment (Docker-safe)

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")