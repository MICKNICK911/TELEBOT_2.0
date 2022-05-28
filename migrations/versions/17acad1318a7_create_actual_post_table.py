"""create actual post table

Revision ID: 17acad1318a7
Revises: de10d3422941
Create Date: 2022-05-28 22:01:44.892143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17acad1318a7'
down_revision = 'de10d3422941'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("memory",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("listen", sa.String(), nullable=False),
                    sa.Column("reply", sa.String(), nullable=False),
                    sa.Column("Author", sa.String(), nullable=False),
                    sa.Column("published", sa.Boolean(), nullable=False, server_default='FALSE'),
                    sa.Column("created", sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text("now()"))
                    )
    pass


def downgrade():
    op.drop_table("memory")
    pass
