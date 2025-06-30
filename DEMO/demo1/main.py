from restgpt.planner import plan
from restgpt.tool_selector import select_tool
from restgpt.caller import generate_tool_args
from restgpt.parser import parse_response
from restgpt.answerer import answer
from tool_calling.tool_manger import ToolManager

from tools.get_weather import get_weather#, get_news, search_web

functions = [get_weather]

tools = ToolManager(functions)

def handle_query(user_query: str):
    tools = ToolManager.get_tools()

    sub_tasks = plan(user_query,tools)
    infos = []

    for task in sub_tasks:
        print("🔍 Task:", task)
        tool_name = task['function']
        # tool_name = select_tool(task,tools)
        args = generate_tool_args(task, tool_name)
        response = ToolManager.call_tool(tool_name, args)
        # info = parse_response(answer)
        infos.append(response)

    llm_answer = answer(infos, user_query)

    return llm_answer

if __name__ == "__main__":
    query = "What is the weather in Paris tomorrow?"
    print(handle_query(query))
