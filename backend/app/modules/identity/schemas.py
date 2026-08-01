from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    display_name: str = Field(min_length=2, max_length=120)
    locale: str = Field(default="en", min_length=2, max_length=35, pattern=r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")

    @field_validator("password")
    @classmethod
    def password_complexity(cls, value: str) -> str:
        classes = sum(
            [
                any(char.islower() for char in value),
                any(char.isupper() for char in value),
                any(char.isdigit() for char in value),
                any(not char.isalnum() for char in value),
            ]
        )
        if classes < 3:
            raise ValueError("Password must use at least three character classes")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class LocaleUpdateRequest(BaseModel):
    locale: str = Field(min_length=2, max_length=35, pattern=r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    display_name: str
    locale: str


class ContextResponse(BaseModel):
    organization_id: UUID
    organization_name: str
    workspace_id: UUID
    workspace_name: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
    context: ContextResponse


class MeResponse(BaseModel):
    user: UserResponse
    context: ContextResponse
