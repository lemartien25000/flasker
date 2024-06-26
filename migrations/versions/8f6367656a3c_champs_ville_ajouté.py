"""champs ville ajouté

Revision ID: 8f6367656a3c
Revises: 85e8a674f7ca
Create Date: 2024-04-14 14:05:58.097123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f6367656a3c'
down_revision = '85e8a674f7ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ville', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('ville')

    # ### end Alembic commands ###
