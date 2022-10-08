"""add content column to posts table

Revision ID: 51d7159e4737
Revises: de82a9bde7b3
Create Date: 2022-10-07 20:00:22.890251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51d7159e4737'
down_revision = 'de82a9bde7b3'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column('posts', sa.Column('content',sa.String, nullable = False ) )
    pass


def downgrade() :
    op.drop_column('posts', 'content')
    pass
