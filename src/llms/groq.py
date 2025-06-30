import requests
import os
from dotenv import load_dotenv

load_dotenv()


class Groq():
    def __init__(self):
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = self.get_model_names()[
            0
        ]  # Default to the first model in the list
        self.default_params = {
            "temperature": 0,
            "max_tokens": 1024,
            "top_p": 1,
            "stream": False,
            "stop": None,
        }

        if not self.api_key:
            raise ValueError("GROQ_API_KEY is missing from environment variables")

    def get_model_names(self) -> list:
        """Return a list of available model names"""
        # llama-3.3-70b-versatile
        return [
            "llama-3.3-70b-versatile",
            "llama3-70b-8192",
        ]

    def set_model(self, model_name: str):
        """Set the model to be used for requests"""
        if model_name not in self.get_model_names():
            raise ValueError(f"Model {model_name} is not available.")
        self.model_name = model_name

    def generate_response(
        self, input_text, use_tools: bool = False, temperature: float = 0.7
    ) -> str:
        """Get response from Groq API using the existing message structure"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        if use_tools:
            pass  # TODO: implement tool usage logic here

        prompt = f"User: {input_text}"

        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": self.model_name,
            **self.default_params,
        }

        response = requests.post(self.api_url, headers=headers, json=payload)
        return self._parse_response(response)

    def _parse_response(self, response: requests.Response) -> str:
        """Handle response parsing with error checking"""
        if response.status_code != 200:
            return f"Error {response.status_code}: {response.text}"

        try:
            return response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            return f"Error parsing response: {str(e)}"



if __name__ == "__main__":
    adapter = Groq()
    # adapter.set_model("llama-3.3-70b-versatile")
    input_text = "What is the capital of France?"
    response = adapter.generate_response(input_text)
    print(f"Response: {response}")