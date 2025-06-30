import inspect
from typing import Dict, List, Any, Callable, Optional,get_type_hints
import re
from tool_calling.tool import Tool

class ToolManager:
    """Class to convert functions to tool format and call them by name."""

    @staticmethod
    def set_tools(functions: List[Callable]):
        """Set tools from a list of functions."""
        tools = ToolManager._convert_functions_to_tools(functions)
        ToolManager.tools = tools
        ToolManager.tool_map = {tool.name: tool for tool in tools}
        
    @staticmethod
    def get_tools() -> List[Tool]:
        """Get the list of tools."""
        return ToolManager.tools
    
    
    @staticmethod
    def _convert_functions_to_tools(functions: List[Callable]) -> List[Tool]:
        tools = []
        
        def infer_type(func: Callable) -> str:
            for name, param in sig.parameters.items():
                default_val = param.default
                inferred_type = type(default_val).__name__ if default_val is not inspect.Parameter.empty else 'unknown'
                print(f"XX (parameter) {name}: {inferred_type}")

        for func in functions:
            sig = inspect.signature(func)
            print(f"Processing function: {func.__name__} with signature: {sig}")
            infer_type(func)

            doc = ToolManager._parse_docstring(func.__doc__)

            parameters = {}
            required_params = []

            for name, param in sig.parameters.items():
                annotation = param.annotation
                param_type = ToolManager._python_type_to_openapi(
                    annotation if annotation != inspect.Parameter.empty else str
                )
                param_info = {
                    "type": param_type,
                    "description": doc["params"].get(name, {}).get("description", ""),
                }

                if param.default is inspect.Parameter.empty:
                    required_params.append(name)

                parameters[name] = param_info

            tool = Tool(
                name=func.__name__,
                description=doc["description"],
                parameters=parameters,
                function=func,
                required_params=required_params,
            )

            tools.append(tool)

        return tools

    @staticmethod
    def _parse_docstring(docstring: Optional[str]) -> Dict[str, Any]:
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
    @staticmethod
    def _python_type_to_openapi(typ: Any) -> str:
        mapping = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
        }
        print(f"Mapping type: {typ} to OpenAPI type")
        if isinstance(typ, type) and typ in mapping:
            return mapping[typ]
        return mapping.get(typ, "string")

    @staticmethod
    def list_tools() -> List[str]:
        return list(ToolManager.tool_map.keys())

    def get_tool_schema(name: str) -> Optional[Dict[str, Any]]:
        tool = ToolManager.tool_map.get(name)
        return tool.to_dict() if tool else None

    @staticmethod
    def call_tool(name: str, arguments: Dict[str, Any]) -> Any:
        tool = ToolManager.tool_map.get(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found.")
        return tool.execute(arguments)

