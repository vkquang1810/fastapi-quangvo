"""add content column to posts table

Revision ID: e332069c4b21
Revises: 9de0abcf08eb
Create Date: 2023-05-31 09:57:53.988139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e332069c4b21'
down_revision = '9de0abcf08eb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
