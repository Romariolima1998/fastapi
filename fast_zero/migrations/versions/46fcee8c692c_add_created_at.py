"""add created_at

Revision ID: 46fcee8c692c
Revises: bb4ef0d449c6
Create Date: 2024-07-18 13:39:22.367779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46fcee8c692c'
down_revision: Union[str, None] = 'bb4ef0d449c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    ...


def downgrade() -> None:
    ...
