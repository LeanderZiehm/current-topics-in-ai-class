from llms.groq import Groq
from agents.utils import clean_llm_json

groq = Groq()

def plan(user_query: str, tools: list) -> list:
    prompt = f"""
You are a task planner that decomposes complex user instructions into a sequence of Python function calls from the ones available:{tools}

Each step should include:
- The function name (snake_case)
- A short description of what it does

If the user request is simple, return just one step.

Output format:
[
  {{
    "function": "function_name",
  }},
  ...
]

User instruction: "{user_query}"
"""
    raw = groq.generate_response(prompt)
    print("🧠 Planner raw:\n", raw)
    return clean_llm_json(raw)
