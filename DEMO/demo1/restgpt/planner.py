from llms.groq import Groq
from restgpt.utils import clean_llm_json

groq = Groq()

def plan(user_query: str):
    prompt = f"""
You are a REST API task planner.

Decompose the following user instruction into a **sequence of REST API steps**.
Each step should:
- Use a REST method like GET, POST, PUT, DELETE
- Include a high-level endpoint path (e.g., /artists/{{id}} or /playlists/{{playlist_id}}/tracks)
- Describe the intent of the step briefly

If only a single step is needed, return just one.

Return the result in JSON format like:
[
  {{
    "method": "GET",
    "endpoint": "/example",
    "description": "Explain what this step does"
  }},
  ...
]

User Request: "{user_query}"
"""
    raw = groq.generate_response(prompt)
    print("🧠 Planner raw output:\n", raw)
    return clean_llm_json(raw)
