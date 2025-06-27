import sqlite3
import requests
import json

# Models
class Models:
    GEMMA3 = 'gemma3'
    GEMMA3_12B = 'gemma3:12b'
    GEMMA3_27B = 'gemma3:27b'
    LLAMA3_8B = 'llama3.1:8b'
    MISTRAL_7B = 'mistral:7b'

# LLM interaction
def generate_text(prompt, model=Models.MISTRAL_7B):
    OLLAMA_BASE_URL = 'https://ollama.leanderziehm.com'
    url = OLLAMA_BASE_URL + '/api/generate'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'model': model,
        'prompt': prompt,
        'stream': False
    }
    response = requests.post(url, json=payload, headers=headers)
    if not response.ok:
        print(f"Failed to generate text: {response.status_code} {response.reason}")
        return {"error": response.reason, "status_code": response.status_code}
    return response.json()


# SQLite setup
def setup_db():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    # Example table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        age INTEGER
                      )''')
    # Insert sample data
    cursor.execute("INSERT OR IGNORE INTO users (id, name, age) VALUES (1, 'Alice', 30)")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, age) VALUES (2, 'Bob', 25)")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, age) VALUES (3, 'Charlie', 35)")
    conn.commit()
    return conn


# Function to ask question and get SQL from LLM
def ask_llm_for_sql(nl_question, schema_description):
    prompt = f"""You are an AI that can write SQLite queries. Given the database schema:

{schema_description}

Generate a valid SQL query that answers the question: "{nl_question}". Only output the SQL, no explanations."""
    
    response = generate_text(prompt)
    return response.get('response', '').strip()


# Execute SQL and return result
def execute_sql(conn, sql_query):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        return [dict(zip(column_names, row)) for row in results]
    except Exception as e:
        return {"error": str(e)}


# Example usage
if __name__ == "__main__":
    conn = setup_db()
    
    # Describe schema to LLM
    schema = """
Table: users
Columns:
- id: INTEGER, primary key
- name: TEXT
- age: INTEGER
"""

    # Natural language question
    question = "Who is the youngest user?"

    # Get SQL from LLM
    sql = ask_llm_for_sql(question, schema)
    print("Generated SQL:", sql)

    # Execute SQL
    result = execute_sql(conn, sql)
    print("Query Result:", json.dumps(result, indent=2))
