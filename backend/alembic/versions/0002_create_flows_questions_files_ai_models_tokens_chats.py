"""create flows, questions, files, ai_models, tokens, chats tables

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-20
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "flows",
        sa.Column("flow_id", sa.String(36), primary_key=True),
        sa.Column("flow_name", sa.String(255), nullable=False),
        sa.Column("flow_user_id", sa.String(36), nullable=False, index=True),
        sa.Column("flow_is_delete", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("public_token", sa.String(36), unique=True, nullable=True, index=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["flow_user_id"], ["users.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "questions",
        sa.Column("question_id", sa.String(36), primary_key=True),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("question_is_last", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("question_parent_id", sa.String(36), nullable=True, index=True),
        sa.Column("question_is_delete", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("question_flow_id", sa.String(36), nullable=False, index=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["question_parent_id"], ["questions.question_id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["question_flow_id"], ["flows.flow_id"], ondelete="CASCADE"
        ),
    )

    op.create_table(
        "files",
        sa.Column("file_id", sa.String(36), primary_key=True),
        sa.Column("flow_file_id", sa.String(36), nullable=False, index=True),
        sa.Column("file_path", sa.String(512), nullable=False),
        sa.Column("file_name", sa.String(255), nullable=False),
        sa.Column("file_size", sa.BigInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column("file_type", sa.String(128), nullable=False, server_default=sa.text("''")),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["flow_file_id"], ["flows.flow_id"], ondelete="CASCADE"),
    )

    op.create_table(
        "ai_models",
        sa.Column("ai_id", sa.String(36), primary_key=True),
        sa.Column("ai_name", sa.String(255), unique=True, nullable=False),
    )

    op.create_table(
        "user_ai_tokens",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), nullable=False, index=True),
        sa.Column("tokens_used", sa.BigInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column("tokens_limit", sa.BigInteger(), nullable=False, server_default=sa.text("100000")),
        sa.Column("period_start", sa.String(10), nullable=False),
        sa.Column("period_end", sa.String(10), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "chats",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("flow_id", sa.String(36), nullable=False, index=True),
        sa.Column("user_id", sa.String(36), nullable=False, index=True),
        sa.Column("title", sa.String(255), nullable=False, server_default=sa.text("''")),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["flow_id"], ["flows.flow_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("chat_id", sa.String(36), nullable=False, index=True),
        sa.Column("role", sa.String(16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.String(32), nullable=False),
        sa.ForeignKeyConstraint(["chat_id"], ["chats.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("chat_messages")
    op.drop_table("chats")
    op.drop_table("user_ai_tokens")
    op.drop_table("ai_models")
    op.drop_table("files")
    op.drop_table("questions")
    op.drop_table("flows")
