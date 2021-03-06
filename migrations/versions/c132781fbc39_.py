"""empty message

Revision ID: c132781fbc39
Revises: 662ddad5fc04
Create Date: 2020-05-21 23:56:24.297964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c132781fbc39'
down_revision = '662ddad5fc04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
    op.drop_column('todos', 'complted')
    # ### end Alembic commands ###
    op.execute('UPDATE todos SET completed = False WHERE completed IS NULL;')
    op.alter_column('todos', 'completed', nullable=False)



def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('complted', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
