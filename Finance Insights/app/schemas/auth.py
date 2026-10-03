from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username_or_email: str
    password: str


class SignupRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    email: str
    password: str
    profile_name: str
    verification_token: str


class EmailRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str


class OtpVerificationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str
    otp: str


class OtpVerificationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    verified: bool
    remaining_attempts: int
    message: str
    token: str | None = None


class AvailabilityResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    available: bool
    message: str


class UserResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    email: str | None
    profile_name: str | None