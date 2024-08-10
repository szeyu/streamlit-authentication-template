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

def create_database():
    # Connect to the default 'postgres' database to create a new database
    conn = psycopg2.connect(dbname="postgres", **{k: v for k, v in db_params.items() if k != "dbname"})
    conn.autocommit = True
    cur = conn.cursor()
    
    # Create the new database
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_params["dbname"])))
    
    cur.close()
    conn.close()

def create_table():
    # Connect to the new database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    """System Prompt
    Create a PostgreSQL table schema for a user management system. The table should have the following columns:

    1. `id`: A primary key of type SERIAL.
    2. `email`: A unique, non-nullable VARCHAR(255) field.
    3. `hash_password`: A non-nullable TEXT field.

    Additionally, include the following columns based on user input parameters:

    <extra_input_params> = {
        
    }

    The generated SQL should be a valid `CREATE TABLE` command in PostgreSQL.
    
    output format:
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        hash_password TEXT NOT NULL,
        <extra_input_param> <extra_input_param type> NOT NULL,
    );

    """
    # Create the table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            hash_password TEXT NOT NULL,
            Faculty TEXT NOT NULL,
            Year INTEGER NOT NULL,
            Semester INTEGER NOT NULL
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    try:
        create_database()
        print("Database created successfully.")
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")

    try:
        create_table()
        print("Table created successfully.")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
