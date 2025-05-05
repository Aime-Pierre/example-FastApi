"""add user table

Revision ID: e66f50bf8ef4
Revises: f6d7734cb6af
Create Date: 2025-05-03 23:33:10.538104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e66f50bf8ef4'
down_revision: Union[str, None] = 'f6d7734cb6af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table('user')
    pass
