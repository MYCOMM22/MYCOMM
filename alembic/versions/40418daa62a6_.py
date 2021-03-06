"""empty message

Revision ID: 40418daa62a6
Revises: 
Create Date: 2022-05-16 00:33:14.921428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40418daa62a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Devices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chip_id', sa.String(), nullable=False),
    sa.Column('mac_id', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('api_key', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Devices')
    # ### end Alembic commands ###
