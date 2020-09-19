"""empty message

Revision ID: 238381617aac
Revises: cc90efededb0
Create Date: 2020-09-18 01:01:12.857100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '238381617aac'
down_revision = 'cc90efededb0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('relationship_historical',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('df_world_id', sa.Integer(), nullable=True),
    sa.Column('hfid1', sa.Integer(), nullable=True),
    sa.Column('hfid2', sa.Integer(), nullable=True),
    sa.Column('love', sa.Integer(), nullable=True),
    sa.Column('respect', sa.Integer(), nullable=True),
    sa.Column('trust', sa.Integer(), nullable=True),
    sa.Column('loyalty', sa.Integer(), nullable=True),
    sa.Column('fear', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['df_world_id'], ['df_world.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vague_relationship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('df_world_id', sa.Integer(), nullable=True),
    sa.Column('hfid1', sa.Integer(), nullable=True),
    sa.Column('hfid2', sa.Integer(), nullable=True),
    sa.Column('war_buddy', sa.Boolean(), nullable=True),
    sa.Column('athlete_buddy', sa.Boolean(), nullable=True),
    sa.Column('athletic_rival', sa.Boolean(), nullable=True),
    sa.Column('childhood_friend', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['df_world_id'], ['df_world.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('relationship', sa.Column('fear', sa.Integer(), nullable=True))
    op.add_column('relationship', sa.Column('love', sa.Integer(), nullable=True))
    op.add_column('relationship', sa.Column('loyalty', sa.Integer(), nullable=True))
    op.add_column('relationship', sa.Column('respect', sa.Integer(), nullable=True))
    op.add_column('relationship', sa.Column('trust', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('relationship', 'trust')
    op.drop_column('relationship', 'respect')
    op.drop_column('relationship', 'loyalty')
    op.drop_column('relationship', 'love')
    op.drop_column('relationship', 'fear')
    op.drop_table('vague_relationship')
    op.drop_table('relationship_historical')
    # ### end Alembic commands ###