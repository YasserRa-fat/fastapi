"""add user table

Revision ID: 1867c2589ba7
Revises: 51d7159e4737
Create Date: 2022-10-07 20:08:00.503460

"""
from tokenize import String
from alembic import op
from pydantic import EmailStr
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1867c2589ba7'
down_revision = '51d7159e4737'
branch_labels = None
depends_on = None


def upgrade() :
    op.create_table( 'users',
                    sa.Column('id', sa.Integer(),nullable = False ),
                    sa.Column('email', sa.String(),nullable = False ),
                    sa.Column('password', sa.String(),nullable = False ),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()')   ,nullable = False ),
                    sa.PrimaryKeyConstraint('id'), 
                    sa.UniqueConstraint('email')
        
        
        
        
    )
    pass


def downgrade() :
    op.drop_table('users')
    
    pass
