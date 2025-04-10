"""
Database utilities for Pokemon SQL Trainer
"""

import psycopg2
from rich.console import Console

console = Console()

# Database connection parameters
DB_PARAMS = {
    'dbname': 'sqlchallenge',
    'user': 'sqlchallenge',
    'password': 'sqlchallenge',
    'host': 'localhost',
    'port': 5432
}

def connect_to_db():
    """Connect to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        return conn
    except Exception as e:
        console.print(f"[bold red]Error connecting to Pokedex database: {e}[/bold red]")
        raise

def execute_query(conn, query_sql):
    """Execute SQL query and return results."""
    cursor = conn.cursor()
    try:
        # Add semicolon if user didn't include one
        if not query_sql.strip().endswith(';'):
            query_sql += ';'
            
        cursor.execute(query_sql)
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            return columns, results
        return None, []
    except Exception as e:
        # Roll back the transaction to clear the error state
        conn.rollback()
        return None, str(e)
    finally:
        cursor.close()

def setup_challenge_database(conn, challenge):
    """Set up database tables and data for a challenge."""
    cursor = conn.cursor()
    try:
        # Reset database - drop all tables in public schema
        cursor.execute("""
            DO $$
            DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """)
        conn.commit()
        
        # Run setup SQL files
        for setup_file in challenge.get('setup', []):
            file_path = os.path.join(challenge['dir'], setup_file.get('file'))
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    setup_sql = f.read()
                cursor.execute(setup_sql)
                conn.commit()
            else:
                console.print(f"[bold red]Error: Setup file {file_path} not found[/bold red]")
                return False
        return True
    except Exception as e:
        console.print(f"[bold red]Error setting up challenge database: {e}[/bold red]")
        return False
    finally:
        cursor.close()

def get_database_schema(conn):
    """Get the database schema information."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """)
        
        schema = {}
        for table, column, dtype in cursor.fetchall():
            if table not in schema:
                schema[table] = []
            schema[table].append((column, dtype))
        
        return schema
    except Exception as e:
        console.print(f"[red]Error retrieving database schema: {e}[/red]")
        return {}
    finally:
        cursor.close()

def get_table_list(conn):
    """Get list of tables in the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        console.print(f"[bold red]Error retrieving table list: {e}[/bold red]")
        return []
    finally:
        cursor.close()

def get_table_data(conn, table_name, limit=100):
    """Get data from a specific table."""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        return columns, results
    except Exception as e:
        console.print(f"[bold red]Error retrieving table data: {e}[/bold red]")
        return None, []
    finally:
        cursor.close()

# Add import at the top of the file
import os
