"""Initial migration.

Revision ID: 44084696cad9
Revises: 
Create Date: 2024-08-09 10:59:01.003259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44084696cad9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resource_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('booking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('resource_id', sa.Integer(), nullable=True),
    sa.Column('booked_at', sa.DateTime(), nullable=False),
    sa.Column('released_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('resource_types')
    with op.batch_alter_table('resource', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.alter_column('resource_type_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('booked_at',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=True)
        batch_op.create_foreign_key('fk_resource_resource_type_id', 'resource_type', ['resource_type_id'], ['id'])
        batch_op.drop_column('description')
        batch_op.drop_column('available_from')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resource', schema=None) as batch_op:
        batch_op.add_column(sa.Column('available_from', sa.DATE(), nullable=False))
        batch_op.add_column(sa.Column('description', sa.VARCHAR(length=200), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('booked_at',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=True)
        batch_op.alter_column('resource_type_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    op.create_table('resource_types',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('booking')
    op.drop_table('resource_type')
    # ### end Alembic commands ###
