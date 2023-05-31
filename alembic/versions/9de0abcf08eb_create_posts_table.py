"""create posts table

Revision ID: 9de0abcf08eb
Revises: 
Create Date: 2023-05-31 09:13:45.083909

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9de0abcf08eb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass