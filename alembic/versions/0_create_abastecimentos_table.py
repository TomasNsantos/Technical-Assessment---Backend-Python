"""create abastecimentos table

Revision ID: b1347c05ea73
Revises:
Create Date: 2026-01-22 00:41:02.187928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1347c05ea73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop existing type if it exists to avoid conflicts
    # This is especially useful during development when the migration 
    # might be run multiple times.
    op.execute("DROP TYPE IF EXISTS tipocombustivel CASCADE")

    # Create the enum type for tipo_combustivel
    # Note: The name 'tipocombustivel' should match the one used in the model
    # to ensure consistency. We shouldn't create it beforehand as SQLAlchemy
    # will handle it when creating the table.

    # Create the abastecimentos table
    # The columns and their types should match those defined in the Abastecimento model.
    op.create_table(
        'abastecimentos',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('id_posto', sa.Integer(), nullable=False),
        sa.Column('data_hora', sa.DateTime(), nullable=False),
        sa.Column(
            'tipo_combustivel',
            sa.Enum('GASOLINA', 'ETANOL', 'DIESEL', name='tipocombustivel'),
            nullable=False
        ),
        sa.Column('preco_por_litro', sa.Numeric(10, 2), nullable=False),
        sa.Column('volume_abastecido', sa.Numeric(10, 2), nullable=False),
        sa.Column('cpf_motorista', sa.String(length=11), nullable=False),
        sa.Column('improper_data', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

    # Create indexes for performance optimization
    op.create_index('ix_abastecimentos_cpf_motorista', 'abastecimentos', ['cpf_motorista'])
    op.create_index('ix_abastecimentos_data_hora', 'abastecimentos', ['data_hora'])



def downgrade() -> None:
    op.drop_index('ix_abastecimentos_data_hora', table_name='abastecimentos')
    op.drop_index('ix_abastecimentos_cpf_motorista', table_name='abastecimentos')
    op.drop_table('abastecimentos')
    op.execute("DROP TYPE tipocombustivel")
