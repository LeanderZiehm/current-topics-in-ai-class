from llms.groq import Groq
from restgpt.utils import clean_llm_json
from tool_calling.tool_manger import ToolManager
import json

groq = Groq()

def generate_api_call(sub_task: dict, api_name: str):
    apis = ToolManager.get_tools()
    api_info = next(api for api in apis if api["name"] == api_name)
    
    prompt = f"""
You are an API caller. You are given a sub-task and an API specification.
Generate valid parameters to call the API based on the sub-task.

Sub-task: {sub_task}

API Spec:
{json.dumps(api_info, indent=2)}

Return the parameters as JSON:
"""
    raw = groq.generate_response(prompt)
    print("📞 Caller raw:", raw)
    return clean_llm_json(raw)
