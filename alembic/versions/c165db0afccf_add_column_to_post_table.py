"""add column to post table

Revision ID: c165db0afccf
Revises: 14ddd684df62
Create Date: 2022-01-29 14:42:38.265544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c165db0afccf'
down_revision = '14ddd684df62'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
