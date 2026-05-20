import uuid

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class File(TimestampMixin, Base):
    __tablename__ = "files"

    file_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    flow_file_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("flows.flow_id", ondelete="CASCADE"), nullable=False, index=True
    )
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    file_type: Mapped[str] = mapped_column(String(128), default="", nullable=False)

    flow: Mapped["Flow"] = relationship("Flow", back_populates="files")
