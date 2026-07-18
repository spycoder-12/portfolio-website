# # import os
# # from pathlib import Path

# # BASE_DIR = Path(__file__).resolve().parent.parent

# # # --- Core ---
# # DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'portfolio.db'}")
# # ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "change-me-please")
# # UPLOAD_DIR = BASE_DIR / "uploads"
# # UPLOAD_DIR.mkdir(exist_ok=True)

# # MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "8"))
# # ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}

# # # --- CORS ---
# # # Comma-separated list of origins allowed to call this API, e.g. "https://mysite.com,http://localhost:5500"
# # CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",")]

# # # --- Email notifications (optional) ---
# # # If SMTP_HOST is unset, the API still saves messages to the database,
# # # it just skips sending an email notification.
# # SMTP_HOST = os.getenv("SMTP_HOST", "")
# # SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
# # SMTP_USER = os.getenv("SMTP_USER", "")
# # SMTP_PASS = os.getenv("SMTP_PASS", "")
# # NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "")  # where new contact submissions get sent

# # # --- Basic contact-form rate limiting (in-memory, per-process) ---
# # CONTACT_RATE_LIMIT_PER_HOUR = int(os.getenv("CONTACT_RATE_LIMIT_PER_HOUR", "5"))



# import os
# from pathlib import Path
# from dotenv import load_dotenv

# # Load variables from .env
# load_dotenv()

# BASE_DIR = Path(__file__).resolve().parent.parent

# # -----------------------------
# # Database
# # -----------------------------
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     f"sqlite:///{BASE_DIR / 'portfolio.db'}"
# )

# # -----------------------------
# # Security
# # -----------------------------
# ADMIN_API_KEY = os.getenv(
#     "ADMIN_API_KEY",
#     "change-me-please"
# )

# # -----------------------------
# # Uploads
# # -----------------------------
# UPLOAD_DIR = BASE_DIR / "uploads"
# UPLOAD_DIR.mkdir(exist_ok=True)

# MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "8"))

# ALLOWED_IMAGE_TYPES = {
#     "image/jpeg",
#     "image/png",
#     "image/webp",
# }

# # -----------------------------
# # CORS
# # -----------------------------
# CORS_ORIGINS = [
#     origin.strip()
#     for origin in os.getenv("CORS_ORIGINS", "*").split(",")
# ]

# # -----------------------------
# # Email
# # -----------------------------
# SMTP_HOST = os.getenv("SMTP_HOST", "")
# SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
# SMTP_USER = os.getenv("SMTP_USER", "")
# SMTP_PASS = os.getenv("SMTP_PASS", "")
# NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "")

# # -----------------------------
# # Contact Form
# # -----------------------------
# CONTACT_RATE_LIMIT_PER_HOUR = int(
#     os.getenv("CONTACT_RATE_LIMIT_PER_HOUR", "5")
# )

# import os
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent

# # --- Core ---
# DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'portfolio.db'}")
# ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "change-me-please")
# UPLOAD_DIR = BASE_DIR / "uploads"
# UPLOAD_DIR.mkdir(exist_ok=True)

# MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "8"))
# ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}

# # --- CORS ---
# # Comma-separated list of origins allowed to call this API, e.g. "https://mysite.com,http://localhost:5500"
# CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",")]

# # --- Email notifications (optional) ---
# # If SMTP_HOST is unset, the API still saves messages to the database,
# # it just skips sending an email notification.
# SMTP_HOST = os.getenv("SMTP_HOST", "")
# SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
# SMTP_USER = os.getenv("SMTP_USER", "")
# SMTP_PASS = os.getenv("SMTP_PASS", "")
# NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "")  # where new contact submissions get sent

# # --- Basic contact-form rate limiting (in-memory, per-process) ---
# CONTACT_RATE_LIMIT_PER_HOUR = int(os.getenv("CONTACT_RATE_LIMIT_PER_HOUR", "5"))



from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

# Points at the folder this file lives in, so portfolio.db and uploads/
# always land next to your code no matter how the project is organized.
BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR / 'portfolio.db'}"
)

# -----------------------------
# Security
# -----------------------------
ADMIN_API_KEY = os.getenv(
    "ADMIN_API_KEY",
    "change-me-please"
)

# -----------------------------
# Uploads
# -----------------------------
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "8"))

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

# -----------------------------
# CORS
# -----------------------------
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "*").split(",")
]

# -----------------------------
# Email
# -----------------------------
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "")

# -----------------------------
# Contact Form
# -----------------------------
CONTACT_RATE_LIMIT_PER_HOUR = int(
    os.getenv("CONTACT_RATE_LIMIT_PER_HOUR", "5")
)