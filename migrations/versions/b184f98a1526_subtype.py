"""subtype

Revision ID: b184f98a1526
Revises: 4f8be17a3e8a
Create Date: 2019-06-19 21:03:16.591097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b184f98a1526'
down_revision = '4f8be17a3e8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('historical_events', sa.Column('subtype', sa.String(length=20), nullable=True))
    #    op.drop_column('historical_events', 'building_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('historical_events', sa.Column('building_id', sa.INTEGER(), nullable=True))
    op.drop_column('historical_events', 'subtype')
    # ### end Alembic commands ###
