"""add foreign-key to post table

Revision ID: 2a3a1b074ebe
Revises: d9c908708747
Create Date: 2025-05-05 14:43:43.586463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a3a1b074ebe'
down_revision: Union[str, None] = 'd9c908708747'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("post", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key(
        "post_user_fk",
        source_table="post",
        referent_table="user",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("post_user_fk", table_name="post")
    op.drop_column("post", "owner_id")
    pass
