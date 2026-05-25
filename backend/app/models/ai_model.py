from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AIModel(Base):
    __tablename__ = "ai_models"

    ai_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    ai_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
