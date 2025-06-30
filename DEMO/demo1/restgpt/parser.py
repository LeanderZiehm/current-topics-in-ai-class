from llms.groq import Groq
from restgpt.utils import clean_llm_json
from tool_calling.tool_manger import ToolManager
import json

groq = Groq()

def parse_response(api_name: str, raw_response: dict):
    apis = ToolManager.get_tools()
    api_info = next(api for api in apis if api["name"] == api_name)
    
    prompt = f"""
You are a response parser. Given an API's response schema and actual JSON result,
generate a concise and human-readable answer.

API: {api_name}
Response Schema: {json.dumps(api_info.get("response_schema", {}), indent=2)}
Raw Response: {json.dumps(raw_response, indent=2)}

Answer:
"""
    return groq.generate_response(prompt).strip()
