"""Added the chapters table

Revision ID: ea41d5eefc7f
Revises: a3574a874f41
Create Date: 2024-12-13 04:02:24.137537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea41d5eefc7f'
down_revision = 'a3574a874f41'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chapters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chapters')
    # ### end Alembic commands ###
