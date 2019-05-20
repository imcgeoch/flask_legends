"""add world and artifacts

Revision ID: 6ff01e4f57c7
Revises: 
Create Date: 2019-05-19 21:06:26.448433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ff01e4f57c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('df_world',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('historical_figures',
    sa.Column('df_world_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['df_world_id'], ['df_world.id'], ),
    sa.PrimaryKeyConstraint('df_world_id', 'id')
    )
    op.create_table('artifacts',
    sa.Column('df_world_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('holder_hfid', sa.Integer(), nullable=True),
    sa.Column('site_id', sa.Integer(), nullable=True),
    sa.Column('structure_local_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['df_world_id', 'holder_hfid'], ['historical_figures.df_world_id', 'historical_figures.id'], ),
    sa.ForeignKeyConstraint(['df_world_id'], ['df_world.id'], ),
    sa.PrimaryKeyConstraint('df_world_id', 'id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artifacts')
    op.drop_table('historical_figures')
    op.drop_table('df_world')
    # ### end Alembic commands ###
