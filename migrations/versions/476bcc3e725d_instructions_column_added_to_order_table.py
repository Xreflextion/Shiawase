"""instructions column added to order table

Revision ID: 476bcc3e725d
Revises: 5d6ffd3f9882
Create Date: 2021-08-16 20:40:09.346572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '476bcc3e725d'
down_revision = '5d6ffd3f9882'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('instructions', sa.String(length=8000), nullable=True))
    op.create_index(op.f('ix_order_dish'), 'order', ['dish'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_dish'), table_name='order')
    op.drop_column('order', 'instructions')
    # ### end Alembic commands ###
