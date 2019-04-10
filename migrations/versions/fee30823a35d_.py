"""empty message

Revision ID: fee30823a35d
Revises: 
Create Date: 2019-04-10 23:56:44.754862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fee30823a35d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('light_spu_qrcode',
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('path', sa.String(length=100), nullable=True),
    sa.Column('spu_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['spu_id'], ['light_spu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_light_spu_spu_num'), 'light_spu', ['spu_num'], unique=True)
    op.drop_index('spu_num', table_name='light_spu')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('spu_num', 'light_spu', ['spu_num'], unique=True)
    op.drop_index(op.f('ix_light_spu_spu_num'), table_name='light_spu')
    op.drop_table('light_spu_qrcode')
    # ### end Alembic commands ###
