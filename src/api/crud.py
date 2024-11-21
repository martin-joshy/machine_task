from sqlmodel import Session, select
from passlib.context import CryptContext

from src.db.models import Profile, ProfileCreate
from src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash the password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


async def create_profile(*, session: Session, profile_create: ProfileCreate) -> Profile:
    """
    Create a new profile in the database

    Args:
        session: Database session
        profile_create: Profile creation data

    Returns:
        Created Profile object
    """
    # Check if email already exists
    # existing_profile = session.exec(
    #     select(Profile).where(Profile.email == profile_create.email)
    # )

    # if existing_profile:
    #     raise ValueError("A profile with this email already exists")

    # Create profile with hashed password
    db_profile = Profile.model_validate(
        profile_create,
        update={"hashed_password": get_password_hash(profile_create.password)},
    )

    await session.add(db_profile)
    await session.commit()
    await session.refresh(db_profile)

    return db_profile


def get_profile_by_email(*, session: Session, email: str) -> Profile | None:
    """
    Retrieve a profile by email

    Args:
        session: Database session
        email: Email to search for

    Returns:
        Profile if found, None otherwise
    """
    statement = select(Profile).where(Profile.email == email)
    return session.exec(statement).first()
