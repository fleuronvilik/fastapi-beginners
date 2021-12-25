"""add content column to posts table

Revision ID: 1ba0d21ade21
Revises: 6e12852def10
Create Date: 2021-12-25 02:02:11.410847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ba0d21ade21'
down_revision = '6e12852def10'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
