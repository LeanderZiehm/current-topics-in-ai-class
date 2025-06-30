from restgpt.planner import plan
from restgpt.tool_selector import select_tool
from restgpt.caller import generate_tool_args
from restgpt.parser import parse_response
from tool_calling.tool_manger import ToolManager

from tools.get_weather import get_weather#, get_news, search_web

functions = [get_weather]

tools = ToolManager(functions)

def handle_query(user_query: str):
    sub_tasks = plan(user_query)
    final_outputs = []
    tools = ToolManager.get_tools()

    for task in sub_tasks:
        
        tool_name = select_tool(task,tools)
        args = generate_tool_args(task, tool_name)
        func = ToolManager.get_function_by_name(tool_name)
        result = func(**args)
        final_output = parse_response(tool_name, result)
        final_outputs.append(final_output)

    return "\n".join(final_outputs)

if __name__ == "__main__":
    query = "What is the weather in Paris tomorrow?"
    print(handle_query(query))
