import asyncio
import logging

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import async_session_factory
from app.models.user import User

logger = logging.getLogger(__name__)

SEED_USERS = [
    {
        "email": "admin@example.com",
        "password": "Admin@123",
        "name": "Admin User",
        "is_active": True,
        "is_superuser": True,
    },
    {
        "email": "user@example.com",
        "password": "User@123",
        "name": "Regular User",
        "is_active": True,
        "is_superuser": False,
    },
]


async def seed_database() -> None:
    async with async_session_factory() as session:
        for user_data in SEED_USERS:
            existing = await session.get(User, user_data["email"])
            if existing:
                logger.info("User %s already exists, skipping", user_data["email"])
                continue
            user = User(
                email=user_data["email"],
                hashed_password=hash_password(user_data["password"]),
                name=user_data["name"],
                is_active=user_data["is_active"],
                is_superuser=user_data["is_superuser"],
            )
            session.add(user)
            logger.info("Created seed user: %s", user_data["email"])
        await session.commit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(seed_database())
