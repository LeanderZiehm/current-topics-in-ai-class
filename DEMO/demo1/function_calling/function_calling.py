import inspect
from typing import Dict, List, Any, Callable, Optional
import re
import json


class Tool_Function:
    """Class to define and execute tool functions for the Groq API."""

    def __init__(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        function: Callable,
        required_params: Optional[List[str]] = None,
    ):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.function = function
        self.required_params = required_params or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": self.parameters,
                "required": self.required_params,
            },
        }

    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        return self.function(**arguments)

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), indent=2)  # str(self.to_dict())

    def __repr__(self) -> str:
        return self.__str__()

def convert_functions_to_tools(functions: List[Callable]) -> List[Tool_Function]:
    tools = []

    for func in functions:
        # func = auto_inject_df(func_raw)
        sig = inspect.signature(func)
        doc = parse_docstring(func.__doc__)

        parameters = {}
        required_params = []

        for name, param in sig.parameters.items():
            annotation = param.annotation
            param_type = python_type_to_openapi(
                annotation if annotation != inspect.Parameter.empty else str
            )
            param_info = {
                "type": param_type,
                "description": doc["params"].get(name, {}).get("description", ""),
            }

            if param.default is inspect.Parameter.empty:
                required_params.append(name)

            parameters[name] = param_info

        tool = Tool_Function(
            name=func.__name__,
            description=doc["description"],
            parameters=parameters,
            function=func,
            required_params=required_params,
        )

        tools.append(tool)

    return tools

def parse_docstring(docstring):
    result = {"description": "", "params": {}}
    if not docstring:
        return result

    lines = docstring.splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    description_lines = []
    parsing_args = False

    for line in lines:
        if line.lower().startswith("args:") or line.lower().startswith("arguments:"):
            parsing_args = True
            continue

        if parsing_args:
            match = re.match(r"(\w+)\s*\(([^)]+)\):\s*(.+)", line)
            if match:
                param, typ, desc = match.groups()
                result["params"][param] = {"type": typ.lower(), "description": desc}
        else:
            description_lines.append(line)

    result["description"] = " ".join(description_lines)
    return result


def python_type_to_openapi(typ):
    mapping = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
    }
    return mapping.get(typ, "string")



def example_usage():

    def greet_user(name: str, age: int):
        """
        Greet a user with their name and age.

        Args:
            name (str): The user's name.
            age (int): The user's age.
        """
        return {"message": f"Hello {name}, you are {age} years old!"}


    def say_goodbye(name: str):
        """
        Say goodbye to a user.

        Args:
            name (str): The user's name.
        """
        return {"message": f"Goodbye {name}!"}


    
    functions = [greet_user, say_goodbye]
    tool_functions = convert_functions_to_tools(functions)
    for tool in tool_functions:
        print(f"\n=== Tool: {tool.name} ===")
        print(tool.to_dict())
        print("= Example Execution =")
        print(
            tool.execute(
                {"name": "Alice", "age": 30}
                if tool.name == "greet_user"
                else {"name": "Alice"}
            )
        )

# Test one
if __name__ == "__main__":
    example_usage()