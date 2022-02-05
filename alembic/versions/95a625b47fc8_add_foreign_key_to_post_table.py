"""add foreign-key to post table

Revision ID: 95a625b47fc8
Revises: 4413d191b2ad
Create Date: 2022-02-05 16:36:58.543405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "95a625b47fc8"
down_revision = "4413d191b2ad"
branch_labels = None
depends_on = None


def upgrade():
    # at first create the column to user table
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer(), nullable=False),
    )
    # here we create the relationship between tow tables
    op.create_foreign_key(
        "post_user_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("post_user_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
