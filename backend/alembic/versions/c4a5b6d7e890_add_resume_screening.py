"""add_resume_screening

Revision ID: c4a5b6d7e890
Revises: b3f2e8c12981
Create Date: 2026-01-28 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c4a5b6d7e890'
down_revision: Union[str, None] = 'b3f2e8c12981'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enums using postgresql dialect for proper control
    resumeparsestatus = postgresql.ENUM(
        'PENDING', 'PARSING', 'PARSED', 'FAILED',
        name='resumeparsestatus',
        create_type=False
    )
    qualificationstatus = postgresql.ENUM(
        'PENDING', 'QUALIFIED', 'NOT_QUALIFIED', 'NEEDS_REVIEW',
        name='qualificationstatus',
        create_type=False
    )

    # Create enum types directly
    conn = op.get_bind()
    resumeparsestatus.create(conn, checkfirst=True)
    qualificationstatus.create(conn, checkfirst=True)

    # Check if parse_status column already exists before adding
    result = conn.execute(sa.text(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name='resumes' AND column_name='parse_status'"
    ))
    if not result.fetchone():
        op.add_column('resumes', sa.Column(
            'parse_status',
            resumeparsestatus,
            nullable=False,
            server_default='PENDING'
        ))
        op.add_column('resumes', sa.Column('parse_error', sa.Text(), nullable=True))

    # Check if table already exists
    result = conn.execute(sa.text(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_name='candidate_job_screenings'"
    ))
    if result.fetchone():
        return  # Table already exists, skip creation

    # Create candidate_job_screenings table
    op.create_table('candidate_job_screenings',
        sa.Column('candidate_id', sa.UUID(), nullable=False),
        sa.Column('job_id', sa.UUID(), nullable=False),
        sa.Column('resume_id', sa.UUID(), nullable=False),
        sa.Column('qualification_status',
            qualificationstatus,
            nullable=False,
            server_default='PENDING'
        ),
        sa.Column('requirement_results', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('gaps', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('gap_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('admin_override', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('override_by_id', sa.UUID(), nullable=True),
        sa.Column('override_reason', sa.Text(), nullable=True),
        sa.Column('override_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('screened_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('screening_notes', sa.Text(), nullable=True),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['override_by_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('candidate_id', 'job_id', name='uq_candidate_job_screening')
    )
    op.create_index(op.f('ix_candidate_job_screenings_candidate_id'), 'candidate_job_screenings', ['candidate_id'], unique=False)
    op.create_index(op.f('ix_candidate_job_screenings_job_id'), 'candidate_job_screenings', ['job_id'], unique=False)
    op.create_index(op.f('ix_candidate_job_screenings_qualification_status'), 'candidate_job_screenings', ['qualification_status'], unique=False)
    op.create_index(op.f('ix_candidate_job_screenings_gap_count'), 'candidate_job_screenings', ['gap_count'], unique=False)


def downgrade() -> None:
    # Drop candidate_job_screenings table
    op.drop_index(op.f('ix_candidate_job_screenings_gap_count'), table_name='candidate_job_screenings')
    op.drop_index(op.f('ix_candidate_job_screenings_qualification_status'), table_name='candidate_job_screenings')
    op.drop_index(op.f('ix_candidate_job_screenings_job_id'), table_name='candidate_job_screenings')
    op.drop_index(op.f('ix_candidate_job_screenings_candidate_id'), table_name='candidate_job_screenings')
    op.drop_table('candidate_job_screenings')

    # Drop columns from resumes table
    op.drop_column('resumes', 'parse_error')
    op.drop_column('resumes', 'parse_status')

    # Drop enums
    op.execute('DROP TYPE IF EXISTS qualificationstatus')
    op.execute('DROP TYPE IF EXISTS resumeparsestatus')
