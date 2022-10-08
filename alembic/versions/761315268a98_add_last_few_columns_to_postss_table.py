"""add last few columns to posts table

Revision ID: 761315268a98
Revises: dd08d7b1f4b8
Create Date: 2022-10-07 20:24:51.352347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '761315268a98'
down_revision = 'dd08d7b1f4b8'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column('posts',
    sa.Column('published', sa.Boolean(), nullable= False, server_default = 'TRUE'))
    op.add_column('posts',sa.Column("created_at" , sa.TIMESTAMP(timezone=True), nullable= False, server_default=sa.text('NOW()')) )
    pass


def downgrade() :
    op.drop_column('posts', column_name="published")
    op.drop_column('posts', column_name="created_at")
    
    pass
