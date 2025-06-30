from llms.groq import Groq
from tool_calling.tool_manger import ToolManager
import json

groq = Groq()

# Step 1: Planner - decompose user query into sub-tasks
def plan(user_query):
    prompt = f"""
You are a task planner. Decompose the following user request into one or more structured sub-tasks in JSON.

User Request: "{user_query}"

Output JSON format:
[
  {{
    "task": "<sub-task description>",
    "location": "<location if any>",
    "date": "<date or relative date like today>"
  }}
]
"""
    response = groq.generate_response(prompt)
    print("Planner response:", response)  # Debugging line
    
    return json.loads(response)

# Step 2: API Selector - choose the best API for each sub-task
def select_api(sub_task):
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
    response = groq.generate_response(prompt)
    return json.loads(response)["api"]

# Step 3: Caller - generate parameters for the selected API
def generate_api_call(sub_task, api_name):
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
    response = groq.generate_response(prompt)
    return json.loads(response)

# Step 4: Execute API call using local function
def execute_api(api_name, params):
    tool_func = ToolManager.get_function_by_name(api_name)
    return tool_func(**params)

# Step 5: Parser - convert raw API response to human-readable output
def parse_response(api_name, raw_response):
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
    return groq.generate_response(prompt)

# Entry Point: Full Workflow
def handle_query(user_query):
    sub_tasks = plan(user_query)
    
    final_outputs = []
    for task in sub_tasks:
        api_name = select_api(task)
        params = generate_api_call(task, api_name)
        raw_response = execute_api(api_name, params)
        human_output = parse_response(api_name, raw_response)
        final_outputs.append(human_output)
    
    return "\n".join(final_outputs)

# # Example usage
# if __name__ == "__main__":
#     query = "What is the weather like in Munich today?"
#     result = handle_query(query)
#     print(result)

if __name__ == "__main__":
    query = "What is the weather like in Munich today?"
    print("📤 Testing LLM planning only...")
    print(plan(query))