"""add_rubric_source_to_scoring_rubrics

Revision ID: 2f95b3dc2402
Revises: 0dedd8de254a
Create Date: 2026-01-26 05:53:51.860801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f95b3dc2402'
down_revision: Union[str, None] = '0dedd8de254a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the enum type first
    rubricsource_enum = sa.Enum('RESEARCH_DEFAULT', 'ROLE_TEMPLATE', 'ORGANIZATION_CUSTOMIZED', 'PROFILING_DERIVED', name='rubricsource')
    rubricsource_enum.create(op.get_bind(), checkfirst=True)

    # Add the column
    op.add_column('scoring_rubrics', sa.Column('rubric_source', rubricsource_enum, nullable=True))


def downgrade() -> None:
    op.drop_column('scoring_rubrics', 'rubric_source')

    # Drop the enum type
    rubricsource_enum = sa.Enum('RESEARCH_DEFAULT', 'ROLE_TEMPLATE', 'ORGANIZATION_CUSTOMIZED', 'PROFILING_DERIVED', name='rubricsource')
    rubricsource_enum.drop(op.get_bind(), checkfirst=True)
