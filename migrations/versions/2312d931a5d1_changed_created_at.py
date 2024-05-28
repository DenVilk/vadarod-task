"""Changed created_at

Revision ID: 2312d931a5d1
Revises: 1b7709d17468
Create Date: 2024-05-28 13:52:37.888987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2312d931a5d1'
down_revision: Union[str, None] = '1b7709d17468'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rates', 'created_at',
               existing_type=sa.DATE(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rates', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=sa.DATE(),
               existing_nullable=True)
    # ### end Alembic commands ###
