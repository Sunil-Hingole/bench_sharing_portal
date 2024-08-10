"""empty message

Revision ID: 3e385820fdb7
Revises: 44084696cad9
Create Date: 2024-08-09 14:52:36.160082

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3e385820fdb7'
down_revision = '44084696cad9'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("PRAGMA foreign_keys = OFF;")

    # Check if resource_tmp table exists before creating it
    op.execute("""
        CREATE TABLE IF NOT EXISTS resource_tmp AS
        SELECT * FROM resource WHERE 1=0;
    """)

    op.execute("""
        INSERT INTO resource_tmp (id, name, resource_type_id, description, available_from, booked_by, booked_at, available, category)
        SELECT id, name, resource_type_id, description, available_from, booked_by, booked_at, available, category
        FROM resource;
    """)

    op.execute("DROP TABLE IF EXISTS resource;")
    
    op.execute("""
        CREATE TABLE resource (
            id INTEGER NOT NULL PRIMARY KEY,
            name VARCHAR(80) NOT NULL,
            resource_type_id INTEGER,
            description VARCHAR(255),
            available_from DATETIME,
            booked_by INTEGER,
            booked_at DATETIME,
            available BOOLEAN,
            category VARCHAR(50) NOT NULL,
            FOREIGN KEY(resource_type_id) REFERENCES resource_type (id),
            FOREIGN KEY(booked_by) REFERENCES user (id)
        );
    """)

    op.execute("""
        INSERT INTO resource (id, name, resource_type_id, description, available_from, booked_by, booked_at, available, category)
        SELECT id, name, resource_type_id, description, available_from, booked_by, booked_at, available,
               COALESCE(category, 'default_category')  -- Use default value if category is null
        FROM resource_tmp;
    """)

    op.execute("DROP TABLE resource_tmp;")
    
    op.execute("PRAGMA foreign_keys = ON;")


def downgrade():
    # Disable foreign key constraints for migration
    op.execute("PRAGMA foreign_keys = OFF;")
    
    # Create temporary table
    op.execute("""
        CREATE TABLE resource_tmp AS SELECT * FROM resource;
    """)

    # Drop the original table
    op.execute("DROP TABLE resource;")
    
    # Recreate the table with the old schema
    op.execute("""
        CREATE TABLE resource (
            id INTEGER NOT NULL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            resource_type_id INTEGER,
            description VARCHAR(200),
            available_from DATE,
            booked_by INTEGER,
            booked_at DATE,
            available BOOLEAN,
            category VARCHAR(50),
            FOREIGN KEY(resource_type_id) REFERENCES resource_type (id),
            FOREIGN KEY(booked_by) REFERENCES user (id)
        );
    """)

    # Copy data from the temporary table to the new table
    op.execute("""
    INSERT INTO resource (id, name, resource_type_id, description, available_from, booked_by, booked_at, available, category)
    SELECT id, name, resource_type_id, description, available_from, booked_by, booked_at, available,
           COALESCE(category, 'default_category')  -- Use default value if category is null
    FROM resource_tmp;
""")


    # Drop the temporary table
    op.execute("DROP TABLE resource_tmp;")
    
    # Re-enable foreign key constraints
    op.execute("PRAGMA foreign_keys = ON;")
