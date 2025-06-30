from llms.groq import Groq
from restgpt.utils import clean_llm_json
from tool_calling.tool_manger import ToolManager
import json

groq = Groq()

def select_tool(task: dict, tools: list):
    tools_str = ToolManager.get_tools_string()


    prompt = f"""
You are a tool selector. Given a task and a list of available Python functions, choose the best function to handle the task.

Task:
{json.dumps(task, indent=2)}

Available Tools:
{tools_str}

Return the best match in JSON:
{{ "tool": "<function_name>" }}
"""
    raw = groq.generate_response(prompt)
    print("🔍 Selector raw:\n", raw)
    return clean_llm_json(raw)["tool"]
