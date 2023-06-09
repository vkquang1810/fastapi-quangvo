"""add user table

Revision ID: 54363b49e2ca
Revises: e332069c4b21
Create Date: 2023-05-31 10:20:24.013514

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '54363b49e2ca'
down_revision = 'e332069c4b21'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')

    pass
