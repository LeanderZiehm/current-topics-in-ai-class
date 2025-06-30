import inspect
from typing import Dict, List, Any, Callable, Optional,Tuple
import re
from tool_calling.tool import Tool

class ToolManager:
    """Class to convert functions to tool format and call them by name."""
    
    def __init__(self, functions: List[Callable]):
        """Initialize ToolManager with a list of functions."""
        ToolManager.set_tools(functions)
        

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
    
    def get_tools_string() -> str:
        """Get a string representation of the tools."""
        return "\n".join([str(tool.to_dict()) for tool in ToolManager.tools])

    
    
    @staticmethod
    def list_tools() -> List[str]:
        return list(ToolManager.tool_map.keys())

    @staticmethod
    def get_tool_schema(name: str) -> Optional[Dict[str, Any]]:
        tool = ToolManager.tool_map.get(name)
        return tool.to_dict() if tool else None

    @staticmethod
    def call_tool(name: str, arguments: Dict[str, Any]) -> Any:
        tool = ToolManager.tool_map.get(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found.")
        return tool.execute(arguments)


    
       
    @staticmethod
    def _infer_parameters_from_function(func: Callable) -> Tuple[Dict[str, Dict[str, Any]], List[str]]:
        """
        Infers parameters info and required parameter names from a function.

        Returns:
            parameters: Dict mapping parameter names to their info (type, description).
            required_params: List of parameter names that are required.
        """
        sig = inspect.signature(func)
        doc = ToolManager._parse_docstring(func.__doc__ or "")

        def infer_type(name: str, param: inspect.Parameter, doc_param: Dict[str, Any]) -> str:
            if param.annotation != inspect.Parameter.empty:
                return ToolManager._python_type_to_openapi(param.annotation)
            if param.default != inspect.Parameter.empty:
                return ToolManager._python_type_to_openapi(type(param.default))
            doc_type = doc_param.get("type")
            if doc_type:
                return doc_type
            return "string"

        parameters = {}
        required_params = []

        for name, param in sig.parameters.items():
            doc_param = doc.get("params", {}).get(name, {})
            param_type = infer_type(name, param, doc_param)

            param_info = {
                "type": param_type,
                "description": doc_param.get("description", ""),
            }

            if param.default is inspect.Parameter.empty:
                required_params.append(name)

            parameters[name] = param_info

        return parameters, required_params

    
    @staticmethod
    def _convert_functions_to_tools(functions: List[Callable]) -> List['Tool']:
        tools = []

        for func in functions:
            # print(f"Processing function: {func.__name__} with signature: {inspect.signature(func)}")

            parameters, required_params = ToolManager._infer_parameters_from_function(func)
            doc = ToolManager._parse_docstring(func.__doc__ or "")

            tool = Tool(
                name=func.__name__,
                description=doc.get("description", ""),
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
        # print(f"Mapping type: {typ} to OpenAPI type")
        if isinstance(typ, type) and typ in mapping:
            return mapping[typ]
        return mapping.get(typ, "string")

