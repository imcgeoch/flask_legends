"""package

Revision ID: b6fbf6b90ab2
Revises: 0a27b4f15153
Create Date: 2019-05-30 21:43:39.860384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6fbf6b90ab2'
down_revision = '0a27b4f15153'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entity_populations')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entity_populations',
    sa.Column('df_world_id', sa.INTEGER(), nullable=False),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('race', sa.VARCHAR(length=20), nullable=True),
    sa.Column('civ_id', sa.INTEGER(), nullable=True),
    sa.Column('num', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['df_world_id'], ['df_world.id'], ),
    sa.PrimaryKeyConstraint('df_world_id', 'id')
    )
    # ### end Alembic commands ###