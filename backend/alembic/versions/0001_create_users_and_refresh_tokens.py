"""create users and refresh_tokens tables

Revision ID: 0001
Revises:
Create Date: 2026-05-20
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column(
            "is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")
        ),
        sa.Column(
            "is_superuser", sa.Boolean(), nullable=False, server_default=sa.text("0")
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("token", sa.Text(), nullable=False, index=True),
        sa.Column("user_id", sa.String(36), nullable=False),
        sa.Column(
            "is_revoked", sa.Boolean(), nullable=False, server_default=sa.text("0")
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
    )


def downgrade() -> None:
    op.drop_table("refresh_tokens")
    op.drop_table("users")
