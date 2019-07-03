"""rem goals

Revision ID: 2b951a799790
Revises: b282e6c7beb2
Create Date: 2019-06-06 18:45:11.526137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b951a799790'
down_revision = 'b282e6c7beb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('goals')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goals',
    sa.Column('df_world_id', sa.INTEGER(), nullable=False),
    sa.Column('hfid', sa.INTEGER(), nullable=False),
    sa.Column('goal', sa.VARCHAR(length=27), nullable=False),
    sa.CheckConstraint("goal IN ('create a great work of art', 'immortality', 'master a skill', 'start a family', 'rule the world', 'fall in love', 'see the great natural sites', 'become a legendary warrior', 'bring peace to the world', 'make a great discovery')"),
    sa.ForeignKeyConstraint(['df_world_id', 'hfid'], ['historical_figures.df_world_id', 'historical_figures.id'], ),
    sa.ForeignKeyConstraint(['df_world_id'], ['df_world.id'], ),
    sa.PrimaryKeyConstraint('df_world_id', 'hfid', 'goal')
    )
    # ### end Alembic commands ###