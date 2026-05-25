from sqlalchemy import BigInteger, Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Question(TimestampMixin, Base):
    __tablename__ = "questions"

    question_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_is_last: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    question_parent_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("questions.question_id", ondelete="SET NULL"), nullable=True, index=True
    )
    question_is_delete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    question_flow_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("flows.flow_id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_button_json: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)

    flow: Mapped["Flow"] = relationship("Flow", back_populates="questions")
    parent: Mapped["Question | None"] = relationship(
        "Question", remote_side="Question.question_id", backref="children"
    )
