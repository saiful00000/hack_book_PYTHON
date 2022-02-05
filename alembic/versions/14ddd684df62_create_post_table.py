"""create post table

Revision ID: 14ddd684df62
Revises: 
Create Date: 2022-01-29 13:25:11.721397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "14ddd684df62"
down_revision = None
branch_labels = None
depends_on = None

# this method upgrade the table as we want to make changes in this table
def upgrade():
    op.create_table(
        "posts",
        sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
