import random
import time
import smtplib
from email.mime.text import MIMEText
from utils.config_loader import load_json_config

# Load SMTP config
email_config = load_json_config("email_config.json")

# Store pending OTPs globally (in-memory)
# key = email, value = dict(otp, username, password_hash, timestamp)
pending_otp = {}
OTP_EXPIRY_SECONDS = 300  # 5 minutes


def generate_otp():
    """Generate a 6-digit OTP string."""
    return str(random.randint(100000, 999999))


def send_otp_email(to_email, otp):
    """Send OTP to the specified email using SMTP config."""
    subject = "Your OTP for FinanceInsights Signup"
    body = f"Dear User,\n\nYour OTP for FinanceInsights signup is:\n\n{otp}\n\n" \
           "This OTP is valid for 5 minutes.\n\nIf you did not request this, please ignore this email.\n\n" \
           "FinanceInsights Team"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = f"{email_config['from_name']} <{email_config['smtp_user']}>"
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL(email_config['smtp_host'], email_config['smtp_port']) as server:
            server.login(email_config['smtp_user'], email_config['smtp_password'])
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        raise Exception(f"SMTP Authentication failed: {e}")
    except Exception as e:
        raise Exception(f"Failed to send OTP email: {e}")


def generate_and_send_otp(email, username=None, password_hash=None):
    """
    Generate a new OTP, store it in pending_otp, and send it via email.
    If OTP already exists for this email, it will be replaced.
    """
    otp = generate_otp()
    pending_otp[email] = {
        "otp": otp,
        "username": username or pending_otp.get(email, {}).get("username"),
        "password_hash": password_hash or pending_otp.get(email, {}).get("password_hash"),
        "timestamp": time.time()
    }

    send_otp_email(email, otp)


def is_otp_valid(email, entered_otp):
    """
    Check if the entered OTP is valid and not expired.
    Returns True if valid, else False.
    """
    data = pending_otp.get(email)
    if not data:
        return False
    if time.time() - data["timestamp"] > OTP_EXPIRY_SECONDS:
        pending_otp.pop(email)
        return False
    return entered_otp == data["otp"]
