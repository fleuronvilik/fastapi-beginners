"""add users table

Revision ID: 5d04877c50fc
Revises: 1ba0d21ade21
Create Date: 2021-12-25 02:07:46.817303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d04877c50fc'
down_revision = '1ba0d21ade21'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
