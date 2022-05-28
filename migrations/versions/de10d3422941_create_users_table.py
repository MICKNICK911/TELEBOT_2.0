"""create post table

Revision ID: de10d3422941
Revises: 
Create Date: 2022-05-28 21:53:39.053144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de10d3422941'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column("trust", sa.Integer(), nullable=False),
                    sa.Column("chat_id", sa.String(), nullable=False),
                    sa.Column("created", sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint('chat_id'),
                    sa.UniqueConstraint('chat_id')
                    )
    pass


def downgrade():
    op.drop_table("users")
    pass
