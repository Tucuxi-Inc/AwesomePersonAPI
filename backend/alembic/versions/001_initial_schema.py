"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-01-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Organizations
    op.create_table(
        'organizations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('website', sa.String(500), nullable=True),
        sa.Column('industry', sa.String(100), nullable=True),
        sa.Column('size', sa.String(50), nullable=True),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('settings', postgresql.JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Users
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), default='INTERVIEWER', nullable=False),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('is_superuser', sa.Boolean, default=False, nullable=False),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('title', sa.String(100), nullable=True),
        sa.Column('bio', sa.Text, nullable=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Traits
    op.create_table(
        'traits',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('category', sa.String(50), nullable=False, index=True),
        sa.Column('definition', sa.Text, nullable=False),
        sa.Column('spectrum_low_label', sa.String(100), nullable=False),
        sa.Column('spectrum_high_label', sa.String(100), nullable=False),
        sa.Column('behavioral_markers_low', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('behavioral_markers_high', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('counter_indicator_for', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('research_foundation', postgresql.JSONB, nullable=True),
        sa.Column('display_order', sa.Integer, default=0, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Trait valence mappings
    op.create_table(
        'trait_valence_mappings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('trait_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('traits.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('role_category', sa.String(100), nullable=False, index=True),
        sa.Column('valence', sa.String(50), nullable=False),
        sa.Column('optimal_range_min', sa.Integer, default=1, nullable=False),
        sa.Column('optimal_range_max', sa.Integer, default=5, nullable=False),
        sa.Column('rationale', sa.Text, nullable=False),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Role profiles
    op.create_table(
        'role_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=True, index=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('department', sa.String(100), nullable=True),
        sa.Column('level', sa.String(50), nullable=True),
        sa.Column('role_category', sa.String(100), nullable=False, index=True),
        sa.Column('critical_traits', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('positive_traits', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('counter_indicators', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('valence_notes', postgresql.JSONB, nullable=True),
        sa.Column('is_template', sa.Boolean, default=False, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('derived_from', postgresql.UUID(as_uuid=True), sa.ForeignKey('role_profiles.id', ondelete='SET NULL'), nullable=True),
        sa.Column('derivation_notes', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Scoring rubrics
    op.create_table(
        'scoring_rubrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=True, index=True),
        sa.Column('role_profile_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('role_profiles.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('trait_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('traits.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('version', sa.Integer, default=1, nullable=False),
        sa.Column('behavioral_anchors', postgresql.JSONB, nullable=False),
        sa.Column('primary_probes', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('follow_up_probes', postgresql.JSONB, nullable=False, default={}),
        sa.Column('star_indicators', postgresql.JSONB, nullable=True),
        sa.Column('is_default', sa.Boolean, default=False, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('derived_from', postgresql.UUID(as_uuid=True), sa.ForeignKey('scoring_rubrics.id', ondelete='SET NULL'), nullable=True),
        sa.Column('derivation_notes', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Scenarios
    op.create_table(
        'scenarios',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('category', sa.String(100), nullable=False, index=True),
        sa.Column('context', sa.Text, nullable=False),
        sa.Column('prompt', sa.Text, nullable=False),
        sa.Column('expected_elements', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('target_traits', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('difficulty_level', sa.Integer, default=3, nullable=False),
        sa.Column('estimated_duration_minutes', sa.Integer, default=15, nullable=False),
        sa.Column('applicable_role_categories', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Top performers
    op.create_table(
        'top_performers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('employee_id', sa.String(100), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('is_anonymized', sa.Boolean, default=False, nullable=False),
        sa.Column('job_title', sa.String(255), nullable=False),
        sa.Column('department', sa.String(100), nullable=True),
        sa.Column('role_category', sa.String(100), nullable=False, index=True),
        sa.Column('tenure_months', sa.Integer, nullable=True),
        sa.Column('performance_metrics', postgresql.JSONB, nullable=True),
        sa.Column('profiling_status', sa.String(50), default='PENDING', nullable=False),
        sa.Column('trait_profile', postgresql.JSONB, nullable=True),
        sa.Column('counter_indicators_identified', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Training sessions
    op.create_table(
        'training_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('top_performer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('top_performers.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('interviewer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('session_number', sa.Integer, default=1, nullable=False),
        sa.Column('status', sa.String(50), default='SCHEDULED', nullable=False),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_minutes', sa.Integer, nullable=True),
        sa.Column('target_traits', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('focus_areas', sa.Text, nullable=True),
        sa.Column('transcript', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('extracted_evidence', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('trait_signals', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('counter_indicators_mentioned', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('interviewer_notes', sa.Text, nullable=True),
        sa.Column('ai_summary', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Candidates
    op.create_table(
        'candidates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('role_profile_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('role_profiles.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('email', sa.String(255), nullable=False, index=True),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('current_title', sa.String(255), nullable=True),
        sa.Column('current_company', sa.String(255), nullable=True),
        sa.Column('linkedin_url', sa.String(500), nullable=True),
        sa.Column('years_experience', sa.Integer, nullable=True),
        sa.Column('source', sa.String(100), nullable=True),
        sa.Column('referrer', sa.String(255), nullable=True),
        sa.Column('status', sa.String(50), default='NEW', nullable=False, index=True),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('tags', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('custom_fields', postgresql.JSONB, nullable=True),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Resumes
    op.create_table(
        'resumes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('candidates.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('file_type', sa.String(50), nullable=False),
        sa.Column('file_size_bytes', sa.Integer, nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('raw_text', sa.Text, nullable=True),
        sa.Column('parsed_data', postgresql.JSONB, nullable=True),
        sa.Column('ai_analysis', postgresql.JSONB, nullable=True),
        sa.Column('version', sa.Integer, default=1, nullable=False),
        sa.Column('is_primary', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Interview sessions
    op.create_table(
        'interview_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('candidates.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('interviewer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('rubric_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scoring_rubrics.id', ondelete='SET NULL'), nullable=True),
        sa.Column('session_number', sa.Integer, default=1, nullable=False),
        sa.Column('session_type', sa.String(50), default='BEHAVIORAL', nullable=False),
        sa.Column('status', sa.String(50), default='SCHEDULED', nullable=False, index=True),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_minutes', sa.Integer, nullable=True),
        sa.Column('target_traits', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('transcript', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('extracted_evidence', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('preliminary_scores', postgresql.JSONB, nullable=True),
        sa.Column('current_trait_index', sa.Integer, default=0, nullable=False),
        sa.Column('probes_used', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('interviewer_notes', sa.Text, nullable=True),
        sa.Column('ai_notes', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Assessment reports
    op.create_table(
        'assessment_reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('candidates.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('role_profile_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('role_profiles.id', ondelete='SET NULL'), nullable=True),
        sa.Column('generated_by_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('version', sa.Integer, default=1, nullable=False),
        sa.Column('status', sa.String(50), default='DRAFT', nullable=False),
        sa.Column('generated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('finalized_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('trait_scores', postgresql.JSONB, nullable=False),
        sa.Column('composite_score', sa.Float, nullable=False),
        sa.Column('composite_explanation', sa.Text, nullable=False),
        sa.Column('recommendation', sa.String(50), nullable=False),
        sa.Column('recommendation_rationale', sa.Text, nullable=False),
        sa.Column('counter_indicator_flags', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('has_counter_indicators', sa.Boolean, default=False, nullable=False),
        sa.Column('key_strengths', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('development_areas', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('interview_summary', sa.Text, nullable=False),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('source_sessions', postgresql.JSONB, nullable=False, default=[]),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Audit logs
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('action', sa.String(100), nullable=False, index=True),
        sa.Column('resource_type', sa.String(100), nullable=False, index=True),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('changes', postgresql.JSONB, nullable=True),
        sa.Column('extra_data', postgresql.JSONB, nullable=True),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('user_agent', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('assessment_reports')
    op.drop_table('interview_sessions')
    op.drop_table('resumes')
    op.drop_table('candidates')
    op.drop_table('training_sessions')
    op.drop_table('top_performers')
    op.drop_table('scenarios')
    op.drop_table('scoring_rubrics')
    op.drop_table('role_profiles')
    op.drop_table('trait_valence_mappings')
    op.drop_table('traits')
    op.drop_table('users')
    op.drop_table('organizations')
