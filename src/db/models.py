import re
import uuid
from typing import Optional

from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel


class ProfileBase(SQLModel):
    """Base model for profile with core attributes"""

    name: str = Field(max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)


class ProfileCreate(ProfileBase):
    """Model for profile creation with password validation"""

    password: str

    @field_validator("password")
    def validate_password(cls, password):
        """
        Validate password against complex policy requirements
        * At least 8 characters long
        * Contains at least one uppercase letter
        * Contains at least one lowercase letter
        * Contains at least one numeric digit
        * Contains at least one special character
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one numeric digit")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character")

        return password


class Profile(ProfileBase, table=True):
    """Database model for storing profile"""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


class ProfilePublic(ProfileBase):
    """Model for returning profile details without sensitive information"""

    id: uuid.UUID


class ProfilesPublic(SQLModel):
    """Model for returning multiple profiles"""

    data: list[ProfilePublic]
    count: int


class Message(SQLModel):
    """Generic message model for API responses"""

    message: str
