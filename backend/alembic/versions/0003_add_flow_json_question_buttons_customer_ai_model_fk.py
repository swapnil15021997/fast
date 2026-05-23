"""add flow_json, question_button_json, customers table, ai_model_fk

Revision ID: 0003
Revises: 0002
Create Date: 2026-05-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("flows", sa.Column("flow_json", sa.Text(), nullable=True))
    op.add_column("flows", sa.Column("flow_connection_json", sa.Text(), nullable=True))
    op.add_column("questions", sa.Column("question_button_json", sa.Text(), nullable=True))
    op.add_column("user_ai_tokens", sa.Column("ai_model_id", sa.String(36), nullable=True, index=True))
    op.create_foreign_key(
        "fk_user_ai_tokens_ai_model",
        "user_ai_tokens", "ai_models",
        ["ai_model_id"], ["ai_id"],
        ondelete="SET NULL",
    )
    op.create_table(
        "customers",
        sa.Column("customer_id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, index=True),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("company", sa.String(255), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by", sa.String(36), nullable=False, index=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("customers")
    op.drop_constraint("fk_user_ai_tokens_ai_model", "user_ai_tokens", type_="foreignkey")
    op.drop_column("user_ai_tokens", "ai_model_id")
    op.drop_column("questions", "question_button_json")
    op.drop_column("flows", "flow_connection_json")
    op.drop_column("flows", "flow_json")
