import uuid

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserAIToken(Base):
    __tablename__ = "user_ai_tokens"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tokens_used: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    tokens_limit: Mapped[int] = mapped_column(BigInteger, default=100000, nullable=False)
    period_start: Mapped[str] = mapped_column(String(10), nullable=False)
    period_end: Mapped[str] = mapped_column(String(10), nullable=False)

    user: Mapped["User"] = relationship("User")
