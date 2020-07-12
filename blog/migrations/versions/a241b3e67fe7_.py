"""empty message

Revision ID: a241b3e67fe7
Revises: ecda71649234
Create Date: 2020-07-11 14:59:55.876334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a241b3e67fe7'
down_revision = 'ecda71649234'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, '人员管理', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, '人员管理', type_='unique')
    # ### end Alembic commands ###
