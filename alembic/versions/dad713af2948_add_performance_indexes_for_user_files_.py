"""Add performance indexes for user files and users

Revision ID: dad713af2948
Revises: 53efef82cf2a
Create Date: 2025-11-29 21:25:16.580912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dad713af2948'
down_revision: Union[str, None] = '53efef82cf2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add indexes for better query performance
    op.create_index('idx_user_files_user_status', 'user_files', ['user_id', 'status', 'created_at DESC'])
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    op.create_index('idx_user_files_user_favorite', 'user_files', ['user_id', 'is_favorite'])
    op.create_index('idx_user_files_created_at', 'user_files', ['created_at DESC'])
    op.create_index('idx_users_created_at', 'users', ['created_at DESC'])


def downgrade() -> None:
    # Remove indexes
    op.drop_index('idx_users_created_at')
    op.drop_index('idx_user_files_created_at')
    op.drop_index('idx_user_files_user_favorite')
    op.drop_index('idx_users_email')
    op.drop_index('idx_user_files_user_status')
