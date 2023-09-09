"""create posts table

Revision ID: 3f15832e3853
Revises: 
Create Date: 2023-09-09 16:23:48.625799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f15832e3853'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('descr', sa.String(), nullable=True))
    pass


def downgrade():
    op.drop_column('posts','descr')
    pass
