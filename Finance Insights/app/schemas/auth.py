from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username_or_email: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    email: str | None
    profile_name: str | None