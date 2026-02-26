"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create farmers table
    op.create_table(
        'farmers',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('phone_number', sa.String(length=15), nullable=False),
        sa.Column('preferred_language', sa.String(length=10), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_active', sa.DateTime(), nullable=False),
        sa.Column('sms_enabled', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_farmers_phone_number'), 'farmers', ['phone_number'], unique=True)

    # Create fields table
    op.create_table(
        'fields',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('farmer_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('crop_type', sa.String(length=50), nullable=False),
        sa.Column('field_size_acres', sa.Float(), nullable=False),
        sa.Column('location_lat', sa.Float(), nullable=False),
        sa.Column('location_lng', sa.Float(), nullable=False),
        sa.Column('pincode', sa.String(length=10), nullable=False),
        sa.Column('irrigation_method', sa.String(length=20), nullable=False),
        sa.Column('planting_date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['farmer_id'], ['farmers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fields_farmer_id'), 'fields', ['farmer_id'], unique=False)

    # Create recommendations table
    op.create_table(
        'recommendations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('field_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('irrigate', sa.Boolean(), nullable=False),
        sa.Column('amount_mm', sa.Float(), nullable=False),
        sa.Column('timing', sa.String(length=20), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('weather_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('reasoning', sa.String(length=500), nullable=False),
        sa.Column('localized_message', sa.String(length=500), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recommendations_field_id'), 'recommendations', ['field_id'], unique=False)
    op.create_index(op.f('ix_recommendations_date'), 'recommendations', ['date'], unique=False)

    # Create irrigation_activities table
    op.create_table(
        'irrigation_activities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('field_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('amount_mm', sa.Float(), nullable=False),
        sa.Column('method', sa.String(length=20), nullable=False),
        sa.Column('farmer_reported', sa.Boolean(), nullable=False),
        sa.Column('cost_rupees', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_irrigation_activities_field_id'), 'irrigation_activities', ['field_id'], unique=False)
    op.create_index(op.f('ix_irrigation_activities_date'), 'irrigation_activities', ['date'], unique=False)

    # Create savings_records table
    op.create_table(
        'savings_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('field_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('period_start', sa.Date(), nullable=False),
        sa.Column('period_end', sa.Date(), nullable=False),
        sa.Column('water_saved_liters', sa.Float(), nullable=False),
        sa.Column('cost_saved_rupees', sa.Float(), nullable=False),
        sa.Column('traditional_usage_liters', sa.Float(), nullable=False),
        sa.Column('actual_usage_liters', sa.Float(), nullable=False),
        sa.Column('calculated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_savings_records_field_id'), 'savings_records', ['field_id'], unique=False)
    op.create_index(op.f('ix_savings_records_period_start'), 'savings_records', ['period_start'], unique=False)
    op.create_index(op.f('ix_savings_records_period_end'), 'savings_records', ['period_end'], unique=False)

    # Create composite indexes for performance optimization
    op.create_index('ix_recommendations_field_date', 'recommendations', ['field_id', 'date'], unique=False)
    op.create_index('ix_irrigation_activities_field_date', 'irrigation_activities', ['field_id', 'date'], unique=False)
    op.create_index('ix_savings_records_field_period', 'savings_records', ['field_id', 'period_start', 'period_end'], unique=False)


def downgrade() -> None:
    # Drop composite indexes
    op.drop_index('ix_savings_records_field_period', table_name='savings_records')
    op.drop_index('ix_irrigation_activities_field_date', table_name='irrigation_activities')
    op.drop_index('ix_recommendations_field_date', table_name='recommendations')

    # Drop tables in reverse order
    op.drop_index(op.f('ix_savings_records_period_end'), table_name='savings_records')
    op.drop_index(op.f('ix_savings_records_period_start'), table_name='savings_records')
    op.drop_index(op.f('ix_savings_records_field_id'), table_name='savings_records')
    op.drop_table('savings_records')

    op.drop_index(op.f('ix_irrigation_activities_date'), table_name='irrigation_activities')
    op.drop_index(op.f('ix_irrigation_activities_field_id'), table_name='irrigation_activities')
    op.drop_table('irrigation_activities')

    op.drop_index(op.f('ix_recommendations_date'), table_name='recommendations')
    op.drop_index(op.f('ix_recommendations_field_id'), table_name='recommendations')
    op.drop_table('recommendations')

    op.drop_index(op.f('ix_fields_farmer_id'), table_name='fields')
    op.drop_table('fields')

    op.drop_index(op.f('ix_farmers_phone_number'), table_name='farmers')
    op.drop_table('farmers')
