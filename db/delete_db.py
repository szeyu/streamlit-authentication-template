import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection parameters
db_params = {
    "dbname":  os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def terminate_connections(dbname):
    conn = psycopg2.connect(dbname="postgres", **{k: v for k, v in db_params.items() if k != "dbname"})
    conn.autocommit = True
    cur = conn.cursor()
    
    # Terminate all connections to the database
    cur.execute(sql.SQL("""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = %s AND pid <> pg_backend_pid();
    """), [dbname])
    
    cur.close()
    conn.close()
    
def drop_table():
    # Connect to the database (replace with default 'postgres' to drop the table)
    conn = psycopg2.connect(dbname="postgres", **{k: v for k, v in db_params.items() if k != "dbname"})
    cur = conn.cursor()

    # Drop the table
    cur.execute("""
        DROP TABLE IF EXISTS users;
    """)

    conn.commit()
    cur.close()
    conn.close()

def drop_database():
    terminate_connections(db_params["dbname"])
    
    # Connect to the default 'postgres' database to drop the database
    conn = psycopg2.connect(dbname="postgres", **{k: v for k, v in db_params.items() if k != "dbname"})
    conn.autocommit = True
    cur = conn.cursor()

    # Drop the database
    cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_params["dbname"])))

    cur.close()
    conn.close()

if __name__ == "__main__":
    try:
        drop_table()
        print("Table deleted successfully.")
    except psycopg2.Error as e:
        print(f"Error deleting table: {e}")

    try:
        drop_database()
        print("Database deleted successfully.")
    except psycopg2.Error as e:
        print(f"Error deleting database: {e}")
