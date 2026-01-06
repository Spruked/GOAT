"""add_unanswered_query_table

Revision ID: ec35008738f2
Revises: dad713af2948
Create Date: 2025-12-02 18:02:49.408059

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec35008738f2'
down_revision: Union[str, None] = 'dad713af2948'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create unanswered_query table
    op.create_table('unanswered_query',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('session_id', sa.String(length=36), nullable=False),
        sa.Column('query_text', sa.Text(), nullable=False),
        sa.Column('query_vec', sa.JSON(), nullable=True),
        sa.Column('skg_clusters_returned', sa.Integer(), nullable=True),
        sa.Column('max_cluster_conf', sa.Float(), nullable=True),
        sa.Column('worker_name', sa.String(length=20), nullable=True),
        sa.Column('vault_reason', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    # Add index on user_id for performance
    op.create_index(op.f('ix_unanswered_query_user_id'), 'unanswered_query', ['user_id'], unique=False)
    # Add index on vault_reason for filtering
    op.create_index(op.f('ix_unanswered_query_vault_reason'), 'unanswered_query', ['vault_reason'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_unanswered_query_vault_reason'), table_name='unanswered_query')
    op.drop_index(op.f('ix_unanswered_query_user_id'), table_name='unanswered_query')
    # Drop table
    op.drop_table('unanswered_query')
