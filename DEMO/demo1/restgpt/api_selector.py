from llms.groq import Groq
from restgpt.utils import clean_llm_json
from tool_calling.tool_manger import ToolManager
import json

groq = Groq()

def select_api(sub_task: dict):
    apis = ToolManager.get_tools()
    apis_str = json.dumps(apis, indent=2)
    
    prompt = f"""
You are an API selector. Choose the best API from the list below to complete the sub-task.

Available APIs:
{apis_str}

Sub-task: {sub_task}

Return the best matching API name in JSON:
{{ "api": "<api_name>" }}
"""
    raw = groq.generate_response(prompt)
    print("🔍 Selector raw:", raw)
    return clean_llm_json(raw)["api"]
