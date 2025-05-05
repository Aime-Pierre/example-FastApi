"""add content column to post table

Revision ID: f6d7734cb6af
Revises: e317a67adff6
Create Date: 2025-05-03 23:28:04.172146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6d7734cb6af'
down_revision: Union[str, None] = 'e317a67adff6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('post', 'content')
    pass
