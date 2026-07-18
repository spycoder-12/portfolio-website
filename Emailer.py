# import smtplib
# import logging
# from email.mime.text import MIMEText

# import config

# logger = logging.getLogger("portfolio.email")


# def send_contact_notification(name: str, email: str, message: str, event_date: str | None):

#     if not config.SMTP_HOST or not config.NOTIFY_EMAIL:
#         logger.info("Email not configured — skipping notification for %s", email)
#         return

#     body = (
#         f"New inquiry from the portfolio site.\n\n"
#         f"Name: {name}\n"
#         f"Email: {email}\n"
#         f"Event date: {event_date or 'Not specified'}\n\n"
#         f"Message:\n{message}\n"
#     )

#     msg = MIMEText(body)
#     msg["Subject"] = f"New portfolio inquiry from {name}"
#     msg["From"] = config.SMTP_USER
#     msg["To"] = config.NOTIFY_EMAIL

#     try:
#         with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=10) as server:
#             server.starttls()

#             if config.SMTP_USER:
#                 server.login(config.SMTP_USER, config.SMTP_PASS)

#             server.sendmail(
#                 msg["From"],
#                 [config.NOTIFY_EMAIL],
#                 msg.as_string()
#             )

#         print("✅ Email sent successfully!")

#     except Exception as exc:
#         print("❌ EMAIL ERROR:", exc)
#         raise

import smtplib
import logging
from email.mime.text import MIMEText

import config

logger = logging.getLogger("portfolio.email")


def send_contact_notification(name: str, email: str, message: str, event_date: str | None):

    print("📩 SEND EMAIL FUNCTION STARTED")

    print("SMTP HOST:", config.SMTP_HOST)
    print("SMTP PORT:", config.SMTP_PORT)
    print("SMTP USER:", config.SMTP_USER)
    print("NOTIFY EMAIL:", config.NOTIFY_EMAIL)

    if not config.SMTP_HOST or not config.NOTIFY_EMAIL:
        print("❌ SMTP CONFIGURATION MISSING")
        return

    body = (
        f"New inquiry from the portfolio site.\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Event date: {event_date or 'Not specified'}\n\n"
        f"Message:\n{message}\n"
    )

    msg = MIMEText(body)

    msg["Subject"] = f"New portfolio inquiry from {name}"
    msg["From"] = config.SMTP_USER
    msg["To"] = config.NOTIFY_EMAIL

    try:
        print("Connecting to SMTP server...")

        with smtplib.SMTP(
            config.SMTP_HOST,
            config.SMTP_PORT,
            timeout=10
        ) as server:

            server.set_debuglevel(1)

            print("Starting TLS...")
            server.starttls()

            print("Logging in...")
            server.login(
                config.SMTP_USER,
                config.SMTP_PASS
            )

            print("Sending email...")

            server.sendmail(
                config.SMTP_USER,
                [config.NOTIFY_EMAIL],
                msg.as_string()
            )

        print("✅ EMAIL SENT SUCCESSFULLY")

    except Exception as e:
        print("❌ EMAIL ERROR:", repr(e))