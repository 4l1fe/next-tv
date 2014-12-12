"""Add column NAME to table Chats

Revision ID: 2edd01ae697
Revises: 531f9b3340b7
Create Date: 2014-12-11 18:36:24.414542

"""

# revision identifiers, used by Alembic.
revision = '2edd01ae697'
down_revision = '531f9b3340b7'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('name', sa.String(length=128), nullable=False, server_default=''))
    op.create_unique_constraint(None, 'chats', ['name'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chats', type_='unique')
    op.drop_column('chats', 'name')
    ### end Alembic commands ###