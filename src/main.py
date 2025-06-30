from agents.planner import plan
from agents.caller import generate_tool_args
from agents.answerer import answer
from tools.tool_manger import ToolManager
from tools.get_weather import get_weather

functions = [get_weather]

tools = ToolManager(functions)

def handle_query(user_query: str):
    tools = ToolManager.get_tools()

    sub_tasks = plan(user_query,tools)
    infos = []

    for task in sub_tasks:
        # print("🔍 Task:", task)
        tool_name = task['function']
        args = generate_tool_args(task, tool_name)
        response = ToolManager.call_tool(tool_name, args)
        infos.append(response)

    llm_answer = answer(infos, user_query)

    return llm_answer

if __name__ == "__main__":
    query = "What is the weather in Paris tomorrow?"
    print(handle_query(query))
