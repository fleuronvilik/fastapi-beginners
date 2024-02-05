"""auto-vote

Revision ID: 1aaca58885ae
Revises: 5eafc10f821d
Create Date: 2021-12-25 23:28:28.369296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1aaca58885ae'
down_revision = '5eafc10f821d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###