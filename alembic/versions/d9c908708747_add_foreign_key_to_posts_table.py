"""add last few columns to posts table

Revision ID: d9c908708747
Revises: e66f50bf8ef4
Create Date: 2025-05-05 00:21:04.202266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9c908708747'
down_revision: Union[str, None] = 'e66f50bf8ef4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "post", 
        sa.Column('published', 
        sa.Boolean(),
        nullable=False, 
        server_default=sa.text("TRUE"),)
        )
    op.add_column(
        "post", 
        sa.Column('created_at', 
        sa.TIMESTAMP(), 
        nullable=False,
        server_default=sa.text("now()"),)
    )
    pass


def downgrade() -> None:
    op.drop_column("post", "published")
    op.drop_column("post", "created_at")
    pass
