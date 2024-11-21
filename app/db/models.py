import re
import uuid
from typing import Optional, Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from sqlmodel import SQLModel, Field as SQLModelField


class ProfileBase(SQLModel):
    """
    Base model for user profile with core attributes.

    Attributes:
        name (str): Full name of the user.
        email (EmailStr): Unique email address for the user.
        phone (Optional[str]): Optional contact phone number.
    """

    name: Annotated[
        str, SQLModelField(max_length=255, description="User's full name")
    ] = "John Doe"

    email: Annotated[
        EmailStr,
        SQLModelField(
            unique=True,
            index=True,
            max_length=255,
            description="Unique email address for user registration",
        ),
    ] = "john@example.com"

    phone: Annotated[
        Optional[str],
        SQLModelField(
            default=None, max_length=20, description="Optional contact phone number"
        ),
    ] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
            }
        }
    )


class ProfileCreate(ProfileBase):
    """
    Model for profile creation with password validation.

    Extends ProfileBase by adding password creation requirements.

    Attributes:
        password (str): User's password with complex requirements.
    """

    password: str = Field(
        description="Password meeting complex security requirements",
        examples=["StrongP@ssword1", "SecurePass123!"],
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, password):
        """
        Validate password against comprehensive security policy.

        Password Requirements:
        - Minimum 8 characters long
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one numeric digit
        - At least one special character (!@#$%^&*(),.?":{}|<>)

        Args:
            password (str): Password to validate

        Raises:
            ValueError: If password does not meet complexity requirements
        """
        password_requirements = [
            (lambda p: len(p) >= 8, "Password must be at least 8 characters long"),
            (
                lambda p: re.search(r"[A-Z]", p),
                "Must contain at least one uppercase letter",
            ),
            (
                lambda p: re.search(r"[a-z]", p),
                "Must contain at least one lowercase letter",
            ),
            (lambda p: re.search(r"\d", p), "Must contain at least one numeric digit"),
            (
                lambda p: re.search(r'[!@#$%^&*(),.?":{}|<>]', p),
                "Must contain at least one special character",
            ),
        ]

        for validator, error_msg in password_requirements:
            if not validator(password):
                raise ValueError(error_msg)

        return password

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "+1234567890",
                    "password": "StrongP@ssword1",
                },
                {
                    "name": "Jane Smith",
                    "email": "jane@example.com",
                    "password": "SecurePass123!",
                },
            ]
        }
    )


class Profile(ProfileBase, table=True):
    """
    Database model for storing user profile details.

    Attributes:
        id (uuid.UUID): Unique profile identifier.
        hashed_password (str): Securely hashed password.
    """

    id: uuid.UUID = SQLModelField(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique profile identifier",
    )
    hashed_password: str = SQLModelField(description="Securely hashed password")


class ProfilePublic(ProfileBase):
    """
    Model for returning profile details without sensitive information.

    Provides a safe representation of profile for public consumption.
    """

    id: uuid.UUID = Field(
        description="Unique profile identifier",
        example="d290f1ee-6c54-4b01-90e6-d701748f0851",
    )


class Message(BaseModel):
    """
    Generic message model for API responses.

    Useful for error handling and informative messages.
    """

    message: str = Field(
        description="Descriptive message about the API response",
        example="A profile with this email already exists",
    )
