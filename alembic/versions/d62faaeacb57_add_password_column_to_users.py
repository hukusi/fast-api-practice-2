"""add password column to users

Revision ID: d62faaeacb57
Revises: a6548be66008
Create Date: 2025-11-01 22:30:26.480369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd62faaeacb57'
down_revision: Union[str, Sequence[str], None] = 'a6548be66008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('users', sa.Column('password', sa.String(), nullable=True))
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))

def downgrade():
    op.drop_column('users', 'role')
    op.drop_column('users', 'password')