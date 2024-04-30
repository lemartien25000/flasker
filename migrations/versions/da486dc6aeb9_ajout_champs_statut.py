"""ajout champs statut

Revision ID: da486dc6aeb9
Revises: 8f6367656a3c
Create Date: 2024-04-15 11:16:48.437894

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'da486dc6aeb9'
down_revision = '8f6367656a3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('statut', sa.String(length=10), nullable=True))
        batch_op.alter_column('ville',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('ville',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
        batch_op.drop_column('statut')

    # ### end Alembic commands ###