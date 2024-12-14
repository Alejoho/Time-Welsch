"""Added the current_chapters table and its relationl with users table

Revision ID: 5733c3dd2f15
Revises: b243d01f19e3
Create Date: 2024-12-14 14:04:15.312502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5733c3dd2f15'
down_revision = 'b243d01f19e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('current_chapters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('current_chapter', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='FK_user_id'),
    sa.PrimaryKeyConstraint('id', name='PK_current_chapters'),
    sa.UniqueConstraint('user_id', name='UQ_user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('current_chapters')
    # ### end Alembic commands ###
