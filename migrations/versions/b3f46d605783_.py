"""empty message

Revision ID: b3f46d605783
Revises: cbc424851d93
Create Date: 2019-04-08 23:39:25.155991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3f46d605783'
down_revision = 'cbc424851d93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('light_spec',
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('spec_num', sa.String(length=50), nullable=False),
    sa.Column('spec_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('spec_name'),
    sa.UniqueConstraint('spec_num')
    )
    op.create_table('light_spec_value',
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('spec_id', sa.Integer(), nullable=True),
    sa.Column('spec_value', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['spec_id'], ['light_spec.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('spec_value')
    )
    op.create_table('light_sku',
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sku_num', sa.String(length=50), nullable=False),
    sa.Column('sku_name', sa.String(length=50), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('spu_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['spu_id'], ['light_spu.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sku_num')
    )
    op.create_table('light_spu_spec',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('spu_id', sa.Integer(), nullable=False),
    sa.Column('spec_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['spec_id'], ['light_spec.id'], ),
    sa.ForeignKeyConstraint(['spu_id'], ['light_spu.id'], ),
    sa.PrimaryKeyConstraint('id', 'spu_id', 'spec_id')
    )
    op.create_table('light_sku_spec',
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sku_id', sa.Integer(), nullable=True),
    sa.Column('spec_value_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sku_id'], ['light_sku.id'], ),
    sa.ForeignKeyConstraint(['spec_value_id'], ['light_spec_value.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('light_sku_spec')
    op.drop_table('light_spu_spec')
    op.drop_table('light_sku')
    op.drop_table('light_spec_value')
    op.drop_table('light_spec')
    # ### end Alembic commands ###
