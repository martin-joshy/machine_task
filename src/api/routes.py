from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Any

import src.api.crud as crud
from src.db.main import get_session
from src.db.models import ProfileCreate, ProfilePublic, Message

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post(
    "/",
    response_model=ProfilePublic,
    status_code=201,
    responses={400: {"model": Message}, 409: {"model": Message}},
)
async def profile(
    *, session: Session = Depends(get_session), profile_in: ProfileCreate
) -> Any:
    """
    Create a new user profile

    - Validates email uniqueness
    - Applies password policy validation
    - Hashes the password before storage

    Raises:
    - 400 Bad Request if email already exists
    - 400 Bad Request if password does not meet policy requirements
    """
    try:
        created_profile = await crud.create_profile(
            session=session, profile_create=profile_in
        )

        return ProfilePublic(
            id=created_profile.id,
            name=created_profile.name,
            email=created_profile.email,
            phone=created_profile.phone,
        )

    except ValueError as e:
        # Handle email already exists or password validation errors
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during profile creation",
        ) from e
