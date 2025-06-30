import inspect
from typing import Dict, List, Any, Callable, Optional, Tuple
import re
import json

class ToolManager:
    """Manages tool functions and their execution."""
    
    tools: List[Dict[str, Any]] = []
    tool_map: Dict[str, Dict[str, Any]] = {}

    def __init__(self, functions: List[Callable]):
        """Initialize ToolManager with a list of functions."""
        self.set_tools(functions)

    @classmethod
    def set_tools(cls, functions: List[Callable]):
        """Convert and store tools from a list of functions."""
        cls.tools = cls._convert_functions_to_tools(functions)
        cls.tool_map = {tool['name']: tool for tool in cls.tools}
        # New: map tool name directly to function
        cls.function_tool_map = {func.__name__: func for func in functions}


    @classmethod
    def get_tools(cls) -> List[Dict[str, Any]]:
        return cls.tools

    @classmethod
    def get_tools_string(cls) -> str:
        return "\n".join([json.dumps(tool, indent=2) for tool in cls.tools])

    @classmethod
    def list_tools(cls) -> List[str]:
        return list(cls.tool_map.keys())

    @classmethod
    def get_tool_schema(cls, name: str) -> Optional[Dict[str, Any]]:
        return cls.tool_map.get(name)

    @classmethod
    def call_tool(cls, name: str, arguments: Dict[str, Any]) -> Any:
        #maybe implement fuzzy matching here
        func = cls.function_tool_map.get(name)
        if not func:
            raise ValueError(f"Tool '{name}' not found.")
        return func(**arguments)


    @classmethod
    def _convert_functions_to_tools(cls, functions: List[Callable]) -> List[Dict[str, Any]]:
        tools = []
        for func in functions:
            params, required = cls._infer_parameters_from_function(func)
            doc = cls._parse_docstring(func.__doc__ or "")
            tools.append({
                "name": func.__name__,
                "description": doc.get("description", ""),
                "parameters": {
                    "type": "object",
                    "properties": params,
                    "required": required,
                }
            })
        return tools

    @classmethod
    def _infer_parameters_from_function(cls, func: Callable) -> Tuple[Dict[str, Dict[str, Any]], List[str]]:
        sig = inspect.signature(func)
        doc = cls._parse_docstring(func.__doc__ or "")

        def infer_type(param: inspect.Parameter, doc_info: Dict[str, Any]) -> str:
            if param.annotation != inspect.Parameter.empty:
                return cls._python_type_to_openapi(param.annotation)
            if param.default != inspect.Parameter.empty:
                return cls._python_type_to_openapi(type(param.default))
            return doc_info.get("type", "string")

        params = {}
        required = []

        for name, param in sig.parameters.items():
            doc_info = doc.get("params", {}).get(name, {})
            param_type = infer_type(param, doc_info)

            params[name] = {
                "type": param_type,
                "description": doc_info.get("description", "")
            }

            if param.default is inspect.Parameter.empty:
                required.append(name)

        return params, required

    @staticmethod
    def _parse_docstring(docstring: str) -> Dict[str, Any]:
        result = {"description": "", "params": {}}
        lines = [line.strip() for line in docstring.splitlines() if line.strip()]

        parsing_args = False
        description_lines = []

        for line in lines:
            if line.lower().startswith("args:") or line.lower().startswith("arguments:"):
                parsing_args = True
                continue
            if parsing_args:
                match = re.match(r"(\w+)\s*\(([^)]+)\):\s*(.+)", line)
                if match:
                    name, typ, desc = match.groups()
                    result["params"][name] = {"type": typ.lower(), "description": desc}
            else:
                description_lines.append(line)

        result["description"] = " ".join(description_lines)
        return result

    @staticmethod
    def _python_type_to_openapi(py_type: Any) -> str:
        mapping = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
        }
        return mapping.get(py_type, "string")
