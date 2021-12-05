"""empty message

Revision ID: a0cecc0d0c77
Revises: b8fa8253371c
Create Date: 2021-12-05 01:01:49.908609

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'a0cecc0d0c77'
down_revision = 'b8fa8253371c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    evilness_types = postgresql.ENUM('evil', 'good', 'neutral', name='evilness_types')
    evilness_types.create(op.get_bind())

    op.add_column('mountain_peaks', sa.Column('is_volcano', sa.Boolean(), nullable=True))
    op.add_column('regions', sa.Column('evilness', sa.Enum('evil', 'good', 'neutral', name='evilness_types'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('regions', 'evilness')
    op.drop_column('mountain_peaks', 'is_volcano')
    # ### end Alembic commands ###