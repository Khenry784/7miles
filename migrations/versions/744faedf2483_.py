"""empty message

Revision ID: 744faedf2483
Revises: e93e653c9109
Create Date: 2021-03-26 05:35:33.532583

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '744faedf2483'
down_revision = 'e93e653c9109'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('add_item', 'pub_date')
    op.drop_column('add_item', 'photo')
    op.drop_column('items', 'unit')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('unit', sa.VARCHAR(length=80), autoincrement=False, nullable=True))
    op.add_column('add_item', sa.Column('photo', sa.VARCHAR(length=150), autoincrement=False, nullable=False))
    op.add_column('add_item', sa.Column('pub_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
