"""add last few column in post table

Revision ID: 96ac11ff47be
Revises: 95a625b47fc8
Create Date: 2022-02-05 17:22:53.601337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "96ac11ff47be"
down_revision = "95a625b47fc8"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_defauls="TRUE"),
    )

    op.add_column(
        "posts",
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")
        ),
    )

    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
