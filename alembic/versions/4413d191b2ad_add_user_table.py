"""add user table

Revision ID: 4413d191b2ad
Revises: c165db0afccf
Create Date: 2022-01-29 20:23:50.838779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4413d191b2ad'
down_revision = 'c165db0afccf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
