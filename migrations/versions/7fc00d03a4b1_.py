"""empty message

Revision ID: 7fc00d03a4b1
Revises: 74dd0d71a280
Create Date: 2019-11-18 03:51:05.625049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fc00d03a4b1'
down_revision = '74dd0d71a280'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_order_info',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('study_Id', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('money', sa.Float(), nullable=False),
    sa.Column('desc', sa.String(length=100), nullable=True),
    sa.Column('order_num', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id', 'study_Id'),
    sa.UniqueConstraint('study_Id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_order_info')
    # ### end Alembic commands ###
