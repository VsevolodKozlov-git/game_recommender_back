"""once again.

Revision ID: 4278d7da4f92
Revises: 4ad02da9efd9
Create Date: 2025-03-25 08:26:27.926664

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '4278d7da4f92'
down_revision: str | None = '4ad02da9efd9'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('game', 'short_description',
               existing_type=sa.VARCHAR(length=2000),
               type_=sa.String(length=5000),
               existing_nullable=True)
    op.drop_constraint('question_survey_id_fkey', 'question', type_='foreignkey')
    op.create_foreign_key(None, 'question', 'survey', ['survey_id'], ['survey_id'], source_schema='public', referent_schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'question', schema='public', type_='foreignkey')
    op.create_foreign_key('question_survey_id_fkey', 'question', 'survey', ['survey_id'], ['survey_id'])
    op.alter_column('game', 'short_description',
               existing_type=sa.String(length=5000),
               type_=sa.VARCHAR(length=2000),
               existing_nullable=True)
    # ### end Alembic commands ###
