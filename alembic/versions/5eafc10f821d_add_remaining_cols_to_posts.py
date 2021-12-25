"""add remaining cols to posts

Revision ID: 5eafc10f821d
Revises: 9bfdbb2c300f
Create Date: 2021-12-25 02:37:35.255851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5eafc10f821d'
down_revision = '9bfdbb2c300f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),)
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),)
    pass


def downgrade():
    op.drop_column("posts", "punlished")
    op.drop_column("posts", "created_at")
    pass
