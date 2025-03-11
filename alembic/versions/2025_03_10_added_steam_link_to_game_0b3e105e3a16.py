"""Added steam link to game.

Revision ID: 0b3e105e3a16
Revises: 03db7f9fc5ae
Create Date: 2025-03-10 21:39:35.901742

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '0b3e105e3a16'
down_revision: str | None = '03db7f9fc5ae'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('question_survey_id_fkey', 'question', type_='foreignkey')
    op.drop_constraint('question_game_id_fkey', 'question', type_='foreignkey')
    op.create_foreign_key(None, 'question', 'survey', ['survey_id'], ['survey_id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'question', 'game', ['game_id'], ['id_game'], source_schema='public', referent_schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'question', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'question', schema='public', type_='foreignkey')
    op.create_foreign_key('question_game_id_fkey', 'question', 'game', ['game_id'], ['id_game'])
    op.create_foreign_key('question_survey_id_fkey', 'question', 'survey', ['survey_id'], ['survey_id'])
    # ### end Alembic commands ###
