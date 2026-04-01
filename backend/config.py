import os

# Reads from environment variables on Render (production)
# Falls back to hardcoded values for local development
SMTP_HOST     = os.environ.get("SMTP_HOST",     "smtp.gmail.com")
SMTP_PORT     = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER     = os.environ.get("SMTP_USER",     "thanmairepalle454@gmail.com")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "qmjycppylrsevvoz")
ADMIN_EMAIL   = os.environ.get("ADMIN_EMAIL",   "ganeshakhila6@gmail.com")
