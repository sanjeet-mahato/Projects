import hashlib
import secrets
from dataclasses import dataclass

from app.services.redis_service import RedisService


@dataclass
class OtpVerificationResult:
    verified: bool
    remaining_attempts: int
    message: str


class OtpService:
    OTP_EXPIRY_SECONDS = 300
    MAX_ATTEMPTS = 3

    def __init__(self):
        self.redis = RedisService()

    @staticmethod
    def generate_otp() -> str:
        return str(
            secrets.randbelow(900000) + 100000
        )

    def store_otp(
        self,
        email: str,
        purpose: str,
        otp: str,
    ) -> None:
        self.redis.set(
            self._get_otp_key(email, purpose),
            self._hash_otp(otp),
            ttl=self.OTP_EXPIRY_SECONDS,
        )

        self.redis.set(
            self._get_attempts_key(email, purpose),
            self.MAX_ATTEMPTS,
            ttl=self.OTP_EXPIRY_SECONDS,
        )

    def verify_otp(
            self,
            email: str,
            purpose: str,
            otp: str,
    ) -> OtpVerificationResult:
        otp_key = self._get_otp_key(email, purpose)
        attempts_key = self._get_attempts_key(email, purpose)

        stored_hash = self.redis.get(otp_key)

        if not stored_hash:
            return OtpVerificationResult(
                verified=False,
                remaining_attempts=0,
                message="OTP expired or not found.",
            )

        if secrets.compare_digest(
                stored_hash,
                self._hash_otp(otp),
        ):
            self.delete_otp(email, purpose)

            return OtpVerificationResult(
                verified=True,
                remaining_attempts=0,
                message="OTP verified successfully.",
            )

        remaining_attempts = int(
            self.redis.get(attempts_key) or 0
        ) - 1

        if remaining_attempts <= 0:
            self.delete_otp(email, purpose)

            return OtpVerificationResult(
                verified=False,
                remaining_attempts=0,
                message="Invalid OTP. Attempts exhausted. Please request a new OTP.",
            )

        self.redis.set(
            attempts_key,
            remaining_attempts,
            ttl=self.OTP_EXPIRY_SECONDS,
        )

        return OtpVerificationResult(
            verified=False,
            remaining_attempts=remaining_attempts,
            message=f"Invalid OTP. Remaining attempts: {remaining_attempts}",
        )

    def delete_otp(
        self,
        email: str,
        purpose: str,
    ) -> None:
        self.redis.delete(
            self._get_otp_key(email, purpose)
        )

        self.redis.delete(
            self._get_attempts_key(email, purpose)
        )

    @staticmethod
    def _hash_otp(otp: str) -> str:
        return hashlib.sha256(
            otp.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _get_otp_key(
            email: str,
        purpose: str,
    ) -> str:
        return f"otp:{purpose}:{email}"

    @staticmethod
    def _get_attempts_key(
            email: str,
        purpose: str,
    ) -> str:
        return f"otp_attempts:{purpose}:{email}"
