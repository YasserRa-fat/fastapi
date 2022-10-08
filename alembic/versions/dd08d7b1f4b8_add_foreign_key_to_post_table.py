"""add foreign key to post table

Revision ID: dd08d7b1f4b8
Revises: 1867c2589ba7
Create Date: 2022-10-07 20:18:12.795292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd08d7b1f4b8'
down_revision = '1867c2589ba7'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column('posts',sa.Column('owner_id', sa.Integer(), nullable= False))  
    op.create_foreign_key('posts_users_fk', source_table='postss', referent_table='users',
                          local_cols= ['owner_id'], remote_cols= ['id'], ondelete='CASCADE')
    
    pass


def downgrade() :
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
