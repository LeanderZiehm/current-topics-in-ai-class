import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_postgres():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def get_schema_description():
    conn = connect_postgres()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)
    rows = cursor.fetchall()
    tables = {}
    for table, col, dtype in rows:
        tables.setdefault(table, []).append((col, dtype))

    schema_output = []
    for table, cols in tables.items():
        schema_output.append(f"📦 Table: {table}")
        for col, dtype in cols:
            schema_output.append(f"  └── {col}: {dtype}")
        schema_output.append("")
    conn.close()
    return "\n".join(schema_output)

if __name__ == "__main__":
    try:
  
    
        schema = get_schema_description()

        print("🧠 Database Schema:\n")
        print(schema)
    except Exception as e:
        print(f"❌ Error: {e}")