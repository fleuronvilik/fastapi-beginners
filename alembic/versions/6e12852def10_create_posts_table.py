"""create posts table

Revision ID: 6e12852def10
Revises: 
Create Date: 2021-12-25 01:47:59.259334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e12852def10'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
