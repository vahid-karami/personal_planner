"""Initial baseline models for projects tasks notes

Revision ID: 4d186b6df56c
Revises: 
Create Date: 2026-07-25 11:02:07.694863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d186b6df56c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
