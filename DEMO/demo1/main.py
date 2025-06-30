from restgpt.planner import plan
from restgpt.api_selector import select_api
from restgpt.caller import generate_api_call
from restgpt.parser import parse_response
from tool_calling.tool_manger import ToolManager

def handle_query(user_query):
    sub_tasks = plan(user_query)
    final_outputs = []

    for task in sub_tasks:
        apis = ToolManager.get_tools()
        api_name = select_api(task)
        params = generate_api_call(task, api_name)
        raw_response = ToolManager.get_function_by_name(api_name)(**params)
        final_output = parse_response(api_name, raw_response)
        final_outputs.append(final_output)

    return "\n".join(final_outputs)

if __name__ == "__main__":
    query = "What is the weather like in Munich today?"
    print(handle_query(query))

