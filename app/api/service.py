from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from app.db.models import Profile, ProfileCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash the password using bcrypt."""
    return pwd_context.hash(password)


class ProfileService:
    """
    Service class for handling profile operations.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize ProfileService with a session.

        Args:
            session (AsyncSession): Database session instance.
        """
        self.session = session

    async def create_profile(self, profile_create: ProfileCreate) -> Profile:
        """
        Create a new profile after validating email uniqueness.

        Args:
            profile_create (ProfileCreate): Data for creating a profile.

        Returns:
            Profile: Created profile object.

        Raises:
            ValueError: If the email is already in use.
        """
        existing_profile = await self.session.exec(
            select(Profile).where(Profile.email == profile_create.email)
        )
        if existing_profile.scalar() is not None:
            raise ValueError("A profile with this email already exists")

        db_profile = Profile.model_validate(
            profile_create,
            update={"hashed_password": get_password_hash(profile_create.password)},
        )

        self.session.add(db_profile)
        await self.session.commit()
        await self.session.refresh(db_profile)

        return db_profile
