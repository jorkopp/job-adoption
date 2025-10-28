import os

class Secrets:
    # Environment-provided secrets (set these in GitHub Actions secrets)
    TWILIO_SID = os.environ.get("TWILIO_SID")
    TWILIO_AUTH = os.environ.get("TWILIO_AUTH")
    TWILIO_FROM = os.environ.get("TWILIO_FROM")
    MY_PHONE = os.environ.get("MY_PHONE")