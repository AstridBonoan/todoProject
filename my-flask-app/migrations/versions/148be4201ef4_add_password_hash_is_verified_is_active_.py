"""Add password_hash, is_verified, is_active, created_at to User

Revision ID: 148be4201ef4
Revises: a5d47a5b6597
Create Date: 2025-07-14 22:39:13.440249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '148be4201ef4'
down_revision = 'a5d47a5b6597'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=True))
        batch_op.add_column(sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('0')))
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('created_at')
        batch_op.drop_column('is_active')
        batch_op.drop_column('is_verified')
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
