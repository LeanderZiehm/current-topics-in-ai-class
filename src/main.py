from agents.planner import plan
from agents.caller import generate_tool_args
from agents.answerer import answer
from tools.tool_manger import ToolManager
from tools.get_weather import get_weather
from tools.get_databse_schema import get_schema_description
from tools.get_disk_usage import get_disk_usage
from tools.search import brave_search

functions = [get_weather, get_schema_description, get_disk_usage, brave_search]

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
    # query = "What is the weather in Paris tomorrow?"
    # query = "What is my disk usage?"
    query = "What new happened today?"
    print(handle_query(query))
