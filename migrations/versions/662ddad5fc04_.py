"""empty message

Revision ID: 662ddad5fc04
Revises: 264682536b02
Create Date: 2020-05-21 23:24:29.436238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '662ddad5fc04'
down_revision = '264682536b02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###
    op.execute('UPDATE todos SET completed = False WHERE completed IS NULL;')
    op.alter_column('todos', 'completed', nullable=False)

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'complted')
    # ### end Alembic commands ###
