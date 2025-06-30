from flask import Flask, render_template, request
from agents.planner import plan
from agents.caller import generate_tool_args
from agents.answerer import answer
from tools.tool_manger import ToolManager
from tools.get_weather import get_weather

app = Flask(__name__)

functions = [get_weather]
ToolManager.set_tools(functions)
tools = ToolManager.get_tools()

query_logs = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_query = request.form.get("user_query", "").strip()
        if not user_query:
            return render_template("index.html", error="Please enter a query.")

        infos = []

        trace = {
            "query": user_query,
            "planner": {"input": user_query, "output": None},
            "caller": [],  # list of dicts: {input: task, output: args, returned: response}
            "answerer": {"input": None, "output": None},
        }

        # Planner
        planner_output = plan(user_query, tools)
        trace["planner"]["output"] = planner_output
        infos.append(planner_output)


        # Caller + Tool calls
        for task in planner_output:
            tool_name = task["function"]
            caller_input = task
            caller_output = generate_tool_args(task, tool_name)
            infos.append(caller_output)
            tool_response = ToolManager.call_tool(tool_name, caller_output)
            trace["caller"].append({
                "tool_name": tool_name,
                "input": caller_input,
                "output": caller_output,
                "returned": tool_response,
            })
            infos.append(tool_response)

        # Answerer
        trace["answerer"]["input"] = {"infos": infos, "user_query": user_query}
        answer_output = answer(infos, user_query)
        trace["answerer"]["output"] = answer_output

        query_logs.append(trace)

        return render_template("result.html", trace=trace)
    else:
        return render_template("index.html")

# @app.route("/logs")
# def logs():
#     return render_template("logs.html", logs=query_logs)

if __name__ == "__main__":
    app.run(debug=True)
