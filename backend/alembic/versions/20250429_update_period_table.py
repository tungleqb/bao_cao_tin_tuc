"""Update Period Table: Add Xa fields and Reports

Revision ID: 20250429_update_period_table
Revises: 27e1d0e0c28c
Create Date: 2025-04-29 11:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '20250429_update_period_table'
down_revision = '27e1d0e0c28c'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('periods', schema=None) as batch_op:
        batch_op.add_column(sa.Column('XaActiveAt', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('XaDeactiveAt', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('XaStartAt', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('XaEndAt', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('XaFromAt', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('XaToAt', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('XaStatus', sa.String(), nullable=False, server_default='Deactive'))

def downgrade():
    with op.batch_alter_table('periods', schema=None) as batch_op:
        batch_op.drop_column('XaStatus')
        batch_op.drop_column('XaToAt')
        batch_op.drop_column('XaFromAt')
        batch_op.drop_column('XaEndAt')
        batch_op.drop_column('XaStartAt')
        batch_op.drop_column('XaDeactiveAt')
        batch_op.drop_column('XaActiveAt')
