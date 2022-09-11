"""empty message

Revision ID: b574b66b2a88
Revises: b172852f5c57
Create Date: 2022-09-11 12:00:41.213886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b574b66b2a88'
down_revision = 'b172852f5c57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('report')
    op.drop_table('post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('image_url', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('author_email', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['author_email'], ['user.email'], name='post_author_email_fkey'),
    sa.PrimaryKeyConstraint('id', name='post_pkey')
    )
    op.create_table('report',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('social_platform', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('account_url', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('image_url', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('reporter_email', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['reporter_email'], ['user.email'], name='report_reporter_email_fkey'),
    sa.PrimaryKeyConstraint('id', name='report_pkey')
    )
    # ### end Alembic commands ###