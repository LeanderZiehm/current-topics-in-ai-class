import os
import psycopg2
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Model list
class Models:
    GEMMA3 = 'gemma3'
    GEMMA3_12B = 'gemma3:12b'
    GEMMA3_27B = 'gemma3:27b'
    LLAMA3_8B = 'llama3.1:8b'
    MISTRAL_7B = 'mistral:7b'

# Send prompt to Ollama LLM
def generate_text(prompt, model=Models.MISTRAL_7B):
    response = requests.post(
        'https://ollama.leanderziehm.com/api/generate',
        json={'model': model, 'prompt': prompt, 'stream': False},
        headers={'Content-Type': 'application/json'}
    )
    if not response.ok:
        raise RuntimeError(f"LLM Error {response.status_code}: {response.reason}")
    return response.json()['response'].strip()

# PostgreSQL connection using env vars
def connect_postgres():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# Fetch all tables & columns from PostgreSQL
def get_schema_description(conn):
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

    desc = []
    for table, cols in tables.items():
        cd = '\n'.join([f"- {col}: {dtype}" for col, dtype in cols])
        desc.append(f"Table: {table}\nColumns:\n{cd}")
    return "\n\n".join(desc)

# Prompt LLM for SQL generation
def ask_llm_for_sql(nl_question, schema_description):
    prompt = f"""You are an AI that writes SQL for PostgreSQL.
Here is the database schema:

{schema_description}

Write an SQL query to answer the question: "{nl_question}"
Output only the SQL. No explanation."""
    return generate_text(prompt)

# Run SQL and return results
def execute_sql(conn, sql_query):
    cur = conn.cursor()
    try:
        cur.execute(sql_query)
    except Exception as e:
        return {"error": str(e)}
    cols = [desc[0] for desc in cur.description] if cur.description else []
    rows = cur.fetchall()
    return [dict(zip(cols, row)) for row in rows]

# Main execution
if __name__ == '__main__':
    conn = connect_postgres()
    schema = get_schema_description(conn)
    print("Detected schema:\n", schema, "\n")

    question = input("Ask your question: ")
    sql = ask_llm_for_sql(question, schema)
    print("\n🔍 Generated SQL:\n", sql, "\n")

    result = execute_sql(conn, sql)
    print("📋 Query Result:")
    print(json.dumps(result, indent=2))

    conn.close()
