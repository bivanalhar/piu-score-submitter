"""add username to Score db

Revision ID: b3b881b91e75
Revises: 866adef73cf3
Create Date: 2022-12-06 11:40:41.223882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3b881b91e75'
down_revision = '866adef73cf3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('score', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=64), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('score', schema=None) as batch_op:
        batch_op.drop_column('username')

    # ### end Alembic commands ###
