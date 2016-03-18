"""empty message

Revision ID: e8862608dd63
Revises: None
Create Date: 2016-03-18 20:02:01.265446

"""

# revision identifiers, used by Alembic.
revision = 'e8862608dd63'
down_revision = None

import sqlalchemy as sa
from alembic import op

statuses = ('sent', 'draft')
status_type = sa.Enum(*statuses, name='status')


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(length=32), nullable=True),
                    sa.Column('pass_hash', sa.String(length=32), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username')
                    )
    op.create_table('mail',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('sender_id', sa.Integer(), nullable=True),
                    sa.Column('recipient_id', sa.Integer(), nullable=True),
                    sa.Column('subject', sa.String(length=128), nullable=True),
                    sa.Column('text', sa.Text(), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.Column('status', status_type, nullable=True),
                    sa.Column('is_viewed', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
                    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('mail_owner',
                    sa.Column('mail_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['mail_id'], ['mail.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('mail_id', 'user_id')
                    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mail_owner')
    op.drop_table('mail')
    op.drop_table('user')
    ### end Alembic commands ###
