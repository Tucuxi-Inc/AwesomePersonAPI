"""add_job_context_to_interview_session

Revision ID: e222b6826761
Revises: c4a5b6d7e890
Create Date: 2026-01-29 04:36:49.254982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e222b6826761'
down_revision: Union[str, None] = 'c4a5b6d7e890'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add job_id and job_context columns to interview_sessions
    op.add_column('interview_sessions', sa.Column('job_id', sa.UUID(), nullable=True))
    op.add_column('interview_sessions', sa.Column('job_context', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.create_index(op.f('ix_interview_sessions_job_id'), 'interview_sessions', ['job_id'], unique=False)
    op.create_foreign_key('fk_interview_sessions_job_id', 'interview_sessions', 'jobs', ['job_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    op.drop_constraint('fk_interview_sessions_job_id', 'interview_sessions', type_='foreignkey')
    op.drop_index(op.f('ix_interview_sessions_job_id'), table_name='interview_sessions')
    op.drop_column('interview_sessions', 'job_context')
    op.drop_column('interview_sessions', 'job_id')
