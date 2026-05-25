from sqlalchemy import BigInteger, Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Flow(TimestampMixin, Base):
    __tablename__ = "flows"

    flow_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    flow_name: Mapped[str] = mapped_column(String(255), nullable=False)
    flow_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    flow_is_delete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    public_token: Mapped[str | None] = mapped_column(
        String(36), unique=True, index=True, nullable=True
    )
    flow_json: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    flow_connection_json: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)

    user: Mapped["User"] = relationship("User")
    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="flow", cascade="all, delete-orphan"
    )
    files: Mapped[list["File"]] = relationship(
        "File", back_populates="flow", cascade="all, delete-orphan"
    )
    chats: Mapped[list["Chat"]] = relationship(
        "Chat", back_populates="flow", cascade="all, delete-orphan"
    )
