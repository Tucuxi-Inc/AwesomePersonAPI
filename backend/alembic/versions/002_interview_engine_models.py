"""Interview engine models for Phase 2.

Revision ID: 002
Revises: 001
Create Date: 2026-01-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create probes table first (referenced by exchanges)
    op.create_table(
        'probes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('session_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('interview_sessions.id', ondelete='CASCADE'),
                  nullable=False, index=True),
        sa.Column('trait_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('traits.id', ondelete='CASCADE'),
                  nullable=False, index=True),
        sa.Column('text', sa.Text, nullable=False),
        sa.Column('probe_type', sa.String(50), nullable=False),
        sa.Column('patterns_applied', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('generation_rationale', sa.Text, nullable=True),
        sa.Column('is_resume_customized', sa.Boolean, default=False, nullable=False),
        sa.Column('resume_anchors', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('base_probe_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('probes.id', ondelete='SET NULL'), nullable=True),
        sa.Column('evidence_expectations', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('follow_up_triggers', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('star_focus', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(),
                  onupdate=sa.func.now(), nullable=False),
    )

    # Create exchanges table
    op.create_table(
        'exchanges',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('session_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('interview_sessions.id', ondelete='CASCADE'),
                  nullable=False, index=True),
        sa.Column('sequence_number', sa.Integer, nullable=False),
        sa.Column('speaker', sa.String(20), nullable=False),
        sa.Column('exchange_type', sa.String(50), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('trait_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('traits.id', ondelete='SET NULL'),
                  nullable=True, index=True),
        sa.Column('probe_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('probes.id', ondelete='SET NULL'), nullable=True),
        sa.Column('analysis_metadata', postgresql.JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(),
                  onupdate=sa.func.now(), nullable=False),
    )

    # Create evidence_items table
    op.create_table(
        'evidence_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('session_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('interview_sessions.id', ondelete='CASCADE'),
                  nullable=False, index=True),
        sa.Column('exchange_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('exchanges.id', ondelete='SET NULL'),
                  nullable=True, index=True),
        sa.Column('trait_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('traits.id', ondelete='CASCADE'),
                  nullable=False, index=True),
        sa.Column('source_type', sa.String(20), nullable=False),
        sa.Column('source_text', sa.Text, nullable=False),
        sa.Column('weight', sa.Float, nullable=False),
        sa.Column('trait_signals', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('star_components', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('confidence', sa.Float, nullable=False, default=0.5),
        sa.Column('specificity_score', sa.Float, nullable=False, default=0.5),
        sa.Column('matched_anchors', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('extraction_rationale', sa.Text, nullable=True),
        sa.Column('contains_conflict', sa.Boolean, default=False, nullable=False),
        sa.Column('contains_failure', sa.Boolean, default=False, nullable=False),
        sa.Column('contains_challenge', sa.Boolean, default=False, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(),
                  onupdate=sa.func.now(), nullable=False),
    )

    # Create trait_assessments table
    op.create_table(
        'trait_assessments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('session_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('interview_sessions.id', ondelete='CASCADE'),
                  nullable=False, index=True),
        sa.Column('trait_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('traits.id', ondelete='CASCADE'),
                  nullable=False, index=True),
        sa.Column('rubric_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('scoring_rubrics.id', ondelete='SET NULL'), nullable=True),
        sa.Column('status', sa.String(30), default='NOT_STARTED', nullable=False),
        sa.Column('raw_score', sa.Integer, nullable=True),
        sa.Column('confidence', sa.Float, default=0.0, nullable=False),
        sa.Column('evidence_count', sa.Integer, default=0, nullable=False),
        sa.Column('behavioral_evidence_count', sa.Integer, default=0, nullable=False),
        sa.Column('star_coverage', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('probes_used_count', sa.Integer, default=0, nullable=False),
        sa.Column('has_primary_probe', sa.Boolean, default=False, nullable=False),
        sa.Column('has_follow_ups', sa.Boolean, default=False, nullable=False),
        sa.Column('has_reflection', sa.Boolean, default=False, nullable=False),
        sa.Column('has_recursion', sa.Boolean, default=False, nullable=False),
        sa.Column('last_response_depth', sa.String(20), nullable=True),
        sa.Column('last_evidence_type', sa.String(20), nullable=True),
        sa.Column('signal_gaps', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('matched_anchors', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('explanation', sa.Text, nullable=True),
        sa.Column('score_rationale', sa.Text, nullable=True),
        sa.Column('patterns_applied', postgresql.JSONB, nullable=False, server_default='[]'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(),
                  onupdate=sa.func.now(), nullable=False),
    )

    # Add new columns to interview_sessions
    op.add_column('interview_sessions',
                  sa.Column('interview_config', postgresql.JSONB, nullable=True))
    op.add_column('interview_sessions',
                  sa.Column('overall_confidence', sa.Float, default=0.0, nullable=False, server_default='0.0'))
    op.add_column('interview_sessions',
                  sa.Column('traits_completed', sa.Integer, default=0, nullable=False, server_default='0'))
    op.add_column('interview_sessions',
                  sa.Column('traits_total', sa.Integer, default=0, nullable=False, server_default='0'))


def downgrade() -> None:
    # Remove new columns from interview_sessions
    op.drop_column('interview_sessions', 'traits_total')
    op.drop_column('interview_sessions', 'traits_completed')
    op.drop_column('interview_sessions', 'overall_confidence')
    op.drop_column('interview_sessions', 'interview_config')

    # Drop tables in reverse order of creation
    op.drop_table('trait_assessments')
    op.drop_table('evidence_items')
    op.drop_table('exchanges')
    op.drop_table('probes')
