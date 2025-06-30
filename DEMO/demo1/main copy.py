from llms.groq import Groq
from DEMO.demo1.tools.get_weather_2 import get_weather
from tool_calling.tool_manger import ToolManager

tools = [get_weather]

ToolManager.set_tools(tools)

print(ToolManager.get_tools())

# [{
#   "name": "get_weather",
#   "description": "",
#   "parameters": {
#     "type": "object",
#     "properties": {
#       "latitude": {
#         "type": "string",
#         "description": ""
#       },
#       "longitude": {
#         "type": "string",
#         "description": ""
#       },
#       "days_ahead": {
#         "type": "string",
#         "description": ""
#       }
#     },
#     "required": []
#   }
# }]

groq = Groq()
response = groq.generate_response(
    "What is the weather like in Munich today?")