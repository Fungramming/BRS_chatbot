"""empty message

Revision ID: f917ce6fe3a2
Revises: 
Create Date: 2018-10-08 11:41:38.495108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f917ce6fe3a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mall',
    sa.Column('idx', sa.Integer(), nullable=False),
    sa.Column('mall_id', sa.String(), nullable=False),
    sa.Column('shop_no', sa.Integer(), nullable=True),
    sa.Column('is_multi_shop', sa.String(), nullable=True),
    sa.Column('lang', sa.String(), nullable=True),
    sa.Column('access_token', sa.String(), nullable=True),
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.Column('expires_at', sa.DateTime(), nullable=True),
    sa.Column('refresh_token_expires_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('idx')
    )
    op.create_table('scripttags',
    sa.Column('idx', sa.Integer(), nullable=False),
    sa.Column('mall_idx', sa.Integer(), nullable=False),
    sa.Column('script_no', sa.Integer(), nullable=True),
    sa.Column('client_id', sa.String(), nullable=False),
    sa.Column('src', sa.String(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('JoinedLocationCode', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['mall_idx'], ['mall.idx'], ),
    sa.PrimaryKeyConstraint('idx'),
    sa.UniqueConstraint('script_no')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scripttags')
    op.drop_table('mall')
    # ### end Alembic commands ###
