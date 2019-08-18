"""image file references

Revision ID: 14ddba349c06
Revises: 34e8738ea9ab
Create Date: 2019-08-17 21:20:14.286873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14ddba349c06'
down_revision = '34e8738ea9ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('site_maps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('df_world_id', sa.Integer(), nullable=True),
    sa.Column('site_id', sa.Integer(), nullable=True),
    sa.Column('path', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['df_world_id'], ['df_world.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('world_maps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('df_world_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.Enum('bm', 'detailed', 'dip', 'drn', 'el', 'elw', 'evil', 'hyd', 'nob', 'rain', 'sal', 'sav', 'str', 'tmp', 'trd', 'veg', 'vol', 'world_map', name='map_types'), nullable=True),
    sa.Column('path', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['df_world_id'], ['df_world.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('world_maps')
    op.drop_table('site_maps')
    # ### end Alembic commands ###
