from llms.groq import Groq
from tool_calling.tool_manger import ToolManager
import json

groq = Groq()

def parse_response(tool_name: str, raw_response: dict):
    tools = ToolManager.get_tools()
    tool_info = next(tool for tool in tools if tool["name"] == tool_name)

    prompt = f"""
You are a response formatter. Given a tool name and its return value, generate a concise human-readable summary.

Tool: {tool_name}
Raw Result: {json.dumps(raw_response, indent=2)}

Answer:
"""
    return groq.generate_response(prompt).strip()
