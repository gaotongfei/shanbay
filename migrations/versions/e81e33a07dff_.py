"""empty message

Revision ID: e81e33a07dff
Revises: a9977d3f0eff
Create Date: 2016-10-01 04:59:20.103547

"""

# revision identifiers, used by Alembic.
revision = 'e81e33a07dff'
down_revision = 'a9977d3f0eff'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    ### end Alembic commands ###
