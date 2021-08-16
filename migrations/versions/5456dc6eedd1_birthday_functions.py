"""birthday functions

Revision ID: 5456dc6eedd1
Revises: f03864302232
Create Date: 2021-08-13 00:52:29.705205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5456dc6eedd1'
down_revision = 'f03864302232'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('bday_celebrated', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'bday_celebrated')
    # ### end Alembic commands ###
