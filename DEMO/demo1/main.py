from llms.groq import Groq
from tools.get_weather import get_weather
from tool_calling.tool_manger import ToolManager

tools = [get_weather]

ToolManager.set_tools(tools)

print(ToolManager.get_tools())

# https://platform.openai.com/docs/guides/function-calling

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