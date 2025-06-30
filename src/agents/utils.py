import json
import re

def clean_llm_json(text: str):
    """
    Extracts the first valid JSON block from a noisy LLM response.
    Ignores preamble or trailing text and returns parsed JSON.
    """
    try:
        json_text_match = re.search(r'\{[\s\S]*?\}|\[[\s\S]*?\]', text)
        if not json_text_match:
            raise ValueError("No valid JSON found.")
        json_text = json_text_match.group(0)
        return json.loads(json_text)
    except Exception as e:
        raise ValueError(f"Failed to clean and parse LLM JSON: {text}") from e
