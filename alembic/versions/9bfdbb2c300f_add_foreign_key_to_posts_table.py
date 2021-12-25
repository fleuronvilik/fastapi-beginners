"""add foreign key to posts table

Revision ID: 9bfdbb2c300f
Revises: 5d04877c50fc
Create Date: 2021-12-25 02:27:29.841073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bfdbb2c300f'
down_revision = '5d04877c50fc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("posts_user_id_fkey",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )
    pass


def downgrade():
    op.drop_constraint("posts_user_id_fkey", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
