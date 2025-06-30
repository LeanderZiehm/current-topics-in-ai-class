from typing import Dict, List, Any, Callable, Optional
import json

class Tool:
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
        return json.dumps(self.to_dict(), indent=2)

    def __repr__(self) -> str:
        return self.__str__()

