from flask import Flask, render_template, request, redirect, url_for

from agents.planner import plan
from agents.caller import generate_tool_args
from agents.answerer import answer
from tools.tool_manger import ToolManager
from tools.get_weather import get_weather

app = Flask(__name__)

# Initialize tools once
functions = [get_weather]
ToolManager.set_tools(functions)
tools = ToolManager.get_tools()

# In-memory log for traceability
query_logs = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_query = request.form.get("user_query", "").strip()
        if not user_query:
            return render_template("index.html", error="Please enter a query.")
        
        # Trace data dict
        trace = {
            "query": user_query,
            "planner_output": None,
            "tool_calls": [],  # list of {tool_name, args, response}
            "final_answer": None,
        }

        # Plan steps
        steps = plan(user_query, tools)
        trace["planner_output"] = steps

        infos = []
        for step in steps:
            tool_name = step["function"]
            args = generate_tool_args(step, tool_name)
            response = ToolManager.call_tool(tool_name, args)
            trace["tool_calls"].append({
                "tool_name": tool_name,
                "args": args,
                "response": response,
            })
            infos.append(response)

        final_answer = answer(infos, user_query)
        trace["final_answer"] = final_answer

        # Store in log
        query_logs.append(trace)

        return render_template("result.html", trace=trace)
    else:
        return render_template("index.html")


@app.route("/logs")
def logs():
    return render_template("logs.html", logs=query_logs)


if __name__ == "__main__":
    app.run(debug=True)
