import smtplib
from email.mime.text import MIMEText

from app.services.apploadconfig import config


class EmailService:
    def __init__(self):
        email_config = config["email"]

        self.smtp_host = email_config["smtp_host"]
        self.smtp_port = email_config["smtp_port"]
        self.smtp_user = email_config["smtp_user"]
        self.smtp_password = email_config["smtp_password"]
        self.sender = email_config["sender"]

    def send_email(
        self,
        subject: str,
        recipients: list[str],
        body: str,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
    ) -> None:
        cc = cc or []
        bcc = bcc or []

        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = f"{self.sender} <{self.smtp_user}>"
        message["To"] = ", ".join(recipients)

        if cc:
            message["Cc"] = ", ".join(cc)

        all_recipients = recipients + cc + bcc

        try:
            with smtplib.SMTP_SSL(
                self.smtp_host,
                self.smtp_port,
            ) as server:
                server.login(
                    self.smtp_user,
                    self.smtp_password,
                )
                server.sendmail(
                    self.smtp_user,
                    all_recipients,
                    message.as_string(),
                )

        except smtplib.SMTPAuthenticationError as exc:
            raise Exception(
                f"SMTP Authentication failed: {exc}"
            ) from exc

        except Exception as exc:
            raise Exception(
                f"Failed to send email: {exc}"
            ) from exc


email_service = EmailService()
