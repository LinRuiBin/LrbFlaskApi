"""empty message

Revision ID: 298c1ab9e065
Revises: 8a01701e599d
Create Date: 2019-02-26 11:56:48.146460

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '298c1ab9e065'
down_revision = '8a01701e599d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book', 'image',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=200),
               existing_nullable=True)
    op.alter_column('gift', 'launched',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('gift', 'launched',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('book', 'image',
               existing_type=sa.String(length=200),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)
    # ### end Alembic commands ###
