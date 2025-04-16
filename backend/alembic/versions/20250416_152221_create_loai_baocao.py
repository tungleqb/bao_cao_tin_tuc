"""create loai_baocao

Revision ID: 20250416_152221
Revises: 
Create Date: 2025-04-16 15:22:21

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250416_152221'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'loai_baocao',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('ten_loai', sa.String(), nullable=False),
        sa.Column('thoi_gian_bat_dau', sa.DateTime(), nullable=False),
        sa.Column('han_gui', sa.DateTime(), nullable=False),
        sa.Column('dinh_ky', sa.Integer(), nullable=False, server_default='0'),
    )


def downgrade():
    op.drop_table('loai_baocao')