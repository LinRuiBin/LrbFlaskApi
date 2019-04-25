"""empty message

Revision ID: bdccf264ddd3
Revises: 
Create Date: 2019-04-24 14:40:51.527327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdccf264ddd3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('adress', sa.Column('addr_status', sa.Integer(), nullable=False))
    op.create_index('idx_user_id_status', 'adress', ['user_id', 'status'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_user_id_status', table_name='adress')
    op.drop_column('adress', 'addr_status')
    # ### end Alembic commands ###