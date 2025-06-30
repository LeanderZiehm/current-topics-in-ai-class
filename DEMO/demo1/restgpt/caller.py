from llms.groq import Groq
from restgpt.utils import clean_llm_json
from tool_calling.tool_manger import ToolManager
import json

groq = Groq()

def generate_tool_args(task: dict, tool_name: str):
    tools = ToolManager.get_tools()
    tool_info = next(tool for tool in tools if tool["name"] == tool_name)

    prompt = f"""
You are a Python function caller. Given a task and a function spec, generate the arguments needed to call the function.

Task:
{json.dumps(task, indent=2)}

Function Spec:
{json.dumps(tool_info, indent=2)}

Return the arguments as a JSON object.
"""
    raw = groq.generate_response(prompt)
    print("📞 Caller raw:\n", raw)
    return clean_llm_json(raw)
