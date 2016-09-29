"""empty message

Revision ID: 496376b1b539
Revises: None
Create Date: 2016-09-29 15:39:48.898456

"""

# revision identifiers, used by Alembic.
revision = '496376b1b539'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('new_user', sa.Integer(), nullable=True),
    sa.Column('words_per_day', sa.Integer(), nullable=True),
    sa.Column('category', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('word',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=100), nullable=False),
    sa.Column('translation', sa.String(length=500), nullable=True),
    sa.Column('category', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_word',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('word_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['word_id'], ['word.id'], )
    )
    op.create_table('user_word_known',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('word_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['word_id'], ['word.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_word_known')
    op.drop_table('user_word')
    op.drop_table('word')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    ### end Alembic commands ###
