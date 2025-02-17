from sqlalchemy import text
from app.db.session import engine


async def drop_all_tables():
    """Drop all tables in the database"""
    async with engine.begin() as conn:
        # Get all table names
        query = """
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public';
        """
        result = await conn.execute(text(query))
        tables = result.scalars().all()

        # Drop each table
        for table in tables:
            await conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE;'))

        # Drop enum types
        enum_query = """
        SELECT t.typname
        FROM pg_type t
        JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
        WHERE t.typtype = 'e' AND n.nspname = 'public';
        """
        enums = await conn.execute(text(enum_query))
        enum_types = enums.scalars().all()

        for enum_type in enum_types:
            await conn.execute(text(f'DROP TYPE IF EXISTS "{enum_type}" CASCADE;'))
