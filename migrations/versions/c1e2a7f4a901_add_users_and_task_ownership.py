"""Add users and task ownership

Revision ID: c1e2a7f4a901
Revises: bb12d8ee0833
Create Date: 2026-07-26 17:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c1e2a7f4a901"
down_revision: Union[str, None] = "bb12d8ee0833"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("1"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_users_id"), ["id"], unique=False)
        batch_op.create_index(batch_op.f("ix_users_username"), ["username"], unique=False)

    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.add_column(sa.Column("owner_id", sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f("ix_tasks_owner_id"), ["owner_id"], unique=False)
        batch_op.create_foreign_key(
            batch_op.f("fk_tasks_owner_id_users"),
            "users",
            ["owner_id"],
            ["id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_tasks_owner_id_users"), type_="foreignkey")
        batch_op.drop_index(batch_op.f("ix_tasks_owner_id"))
        batch_op.drop_column("owner_id")

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_users_username"))
        batch_op.drop_index(batch_op.f("ix_users_id"))

    op.drop_table("users")
