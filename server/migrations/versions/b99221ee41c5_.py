"""empty message

Revision ID: b99221ee41c5
Revises: 7450fc7ffbdb
Create Date: 2023-12-11 13:50:00.274167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b99221ee41c5'
down_revision = '7450fc7ffbdb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('receivers_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('gifts_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('receiver_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_gifts_table_receiver_id_receivers_table'), 'receivers_table', ['receiver_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gifts_table', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_gifts_table_receiver_id_receivers_table'), type_='foreignkey')
        batch_op.drop_column('receiver_id')

    op.drop_table('receivers_table')
    # ### end Alembic commands ###