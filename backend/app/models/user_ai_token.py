from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserAIToken(Base):
    __tablename__ = "user_ai_tokens"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    ai_model_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("ai_models.ai_id", ondelete="SET NULL"), nullable=True, index=True
    )
    ai_token: Mapped[str | None] = mapped_column(String(512), nullable=True)
    tokens_used: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    tokens_limit: Mapped[int] = mapped_column(BigInteger, default=100000, nullable=False)
    period_start: Mapped[str] = mapped_column(String(10), nullable=False)
    period_end: Mapped[str] = mapped_column(String(10), nullable=False)

    user: Mapped["User"] = relationship("User")
    ai_model: Mapped["AIModel | None"] = relationship("AIModel")
