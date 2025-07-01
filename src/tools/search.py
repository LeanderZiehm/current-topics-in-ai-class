import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Brave API key from environment
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

def brave_search(query, count=5):
    """
    Search the web using the Brave Search API.

    Args:
        query (str): The search query string.
        count (int): Number of results to return (default is 5).

    Returns:
        str: Formatted string with top search results.
    """
    if not BRAVE_API_KEY:
        return "Error: BRAVE_API_KEY is not set in the environment."

    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    params = {
        "q": query,
        "count": count
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return f"Error: API request failed with status code {response.status_code}\n{response.text}"

    data = response.json()
    results = data.get("web", {}).get("results", [])

    if not results:
        return "No results found."

    output = f"Top {len(results)} search results for '{query}':\n\n"
    for idx, item in enumerate(results, 1):
        title = item.get("title", "No title")
        url = item.get("url", "No URL")
        description = item.get("description", "No description")
        output += f"{idx}. {title}\n   {url}\n   {description}\n\n"

    return output.strip()


if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    print(brave_search(search_query))
