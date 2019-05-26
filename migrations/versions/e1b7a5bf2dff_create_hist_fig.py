"""create hist_fig

Revision ID: e1b7a5bf2dff
Revises: 854a2e07f184
Create Date: 2019-05-20 20:16:28.910565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1b7a5bf2dff'
down_revision = '854a2e07f184'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('historical_figures', sa.Column('active_interaction', sa.String(length=50), nullable=True))
    op.add_column('historical_figures', sa.Column('animated', sa.Boolean(), nullable=True))
    op.add_column('historical_figures', sa.Column('animated_string', sa.String(length=50), nullable=True))
    op.add_column('historical_figures', sa.Column('appeared', sa.Integer(), nullable=True))
    op.add_column('historical_figures', sa.Column('associated_type', sa.String(length=20), nullable=True))
    op.add_column('historical_figures', sa.Column('birth_seconds72', sa.Integer(), nullable=True))
    op.add_column('historical_figures', sa.Column('birth_year', sa.Integer(), nullable=True))
    op.add_column('historical_figures', sa.Column('caste', sa.String(length=10), nullable=True))
    op.add_column('historical_figures', sa.Column('current_identity_id', sa.Integer(), nullable=True))
    op.add_column('historical_figures', sa.Column('death_seconds72', sa.Integer(), nullable=True))
    op.add_column('historical_figures', sa.Column('death_year', sa.Integer(), nullable=True))
    op.add_column('historical_figures', sa.Column('deity', sa.Boolean(), nullable=True))
    op.add_column('historical_figures', sa.Column('ent_pop_id', sa.Integer(), nullable=True))
    op.add_column('historical_figures', sa.Column('force', sa.Boolean(), nullable=True))
    op.add_column('historical_figures', sa.Column('name', sa.String(length=50), nullable=True))
    op.add_column('historical_figures', sa.Column('race', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('historical_figures', 'race')
    op.drop_column('historical_figures', 'name')
    op.drop_column('historical_figures', 'force')
    op.drop_column('historical_figures', 'ent_pop_id')
    op.drop_column('historical_figures', 'deity')
    op.drop_column('historical_figures', 'death_year')
    op.drop_column('historical_figures', 'death_seconds72')
    op.drop_column('historical_figures', 'current_identity_id')
    op.drop_column('historical_figures', 'caste')
    op.drop_column('historical_figures', 'birth_year')
    op.drop_column('historical_figures', 'birth_seconds72')
    op.drop_column('historical_figures', 'associated_type')
    op.drop_column('historical_figures', 'appeared')
    op.drop_column('historical_figures', 'animated_string')
    op.drop_column('historical_figures', 'animated')
    op.drop_column('historical_figures', 'active_interaction')
    # ### end Alembic commands ###