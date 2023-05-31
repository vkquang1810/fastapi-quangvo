"""add foreign-key to posts table

Revision ID: c0a17d2dc7e5
Revises: 54363b49e2ca
Create Date: 2023-05-31 10:46:14.575372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0a17d2dc7e5'
down_revision = '54363b49e2ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table='users', local_cols=['owner_id'],
                          remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
