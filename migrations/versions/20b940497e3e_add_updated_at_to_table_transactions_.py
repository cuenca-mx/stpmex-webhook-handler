"""Add updated_at to table transactions and make estado an enum

Revision ID: 20b940497e3e
Revises: 447a38e07c4e
Create Date: 2018-10-04 11:19:47.394403

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '20b940497e3e'
down_revision = '447a38e07c4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions',
                  sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'updated_at')
    # ### end Alembic commands ###
