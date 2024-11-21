from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from sqlmodel.ext.asyncio.session import AsyncSession

import app.api.service as service
from app.db.main import get_session
from app.db.models import ProfileCreate, ProfilePublic, Message

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post(
    "/",
    response_model=ProfilePublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Profile successfully created",
            "model": ProfilePublic,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid profile data",
            "model": Message,
        },
        status.HTTP_409_CONFLICT: {
            "description": "Email already registered",
            "model": Message,
        },
    },
    summary="Create a new user profile",
    description="""
    Create a new user profile with comprehensive validation:
    - Unique email registration
    - Complex password requirements
    - Optional phone number

    Password Policy:
    - Minimum 8 characters
    - Must include uppercase and lowercase letters
    - Must include at least one number
    - Must include at least one special character
    """,
)
async def create_profile(
    *, session: Annotated[AsyncSession, Depends(get_session)], profile_in: ProfileCreate
) -> ProfilePublic:
    """
    Create a new user profile with comprehensive validation.

    Args:
        session (AsyncSession): Database session dependency
        profile_in (ProfileCreate): Profile creation request data

    Returns:
        ProfilePublic: Created profile details without sensitive information

    Raises:
        HTTPException: 400 for validation errors, 500 for unexpected errors
    """
    try:
        created_profile = await service.ProfileService(session).create_profile(
            profile_create=profile_in
        )

        return ProfilePublic.model_validate(created_profile)

    except ValueError as e:
        # Specific handling for validation errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except Exception as e:
        print(e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during profile creation",
        ) from e
