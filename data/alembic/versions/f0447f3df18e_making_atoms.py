"""making atoms

Revision ID: f0447f3df18e
Revises: e24eefb81e98
Create Date: 2022-01-01 18:42:43.571605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0447f3df18e'
down_revision = 'e24eefb81e98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('atoms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('x', sa.Float(), nullable=True),
                    sa.Column('y', sa.Float(), nullable=True),
                    sa.Column('z', sa.Float(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('atoms')
    # ### end Alembic commands ###
