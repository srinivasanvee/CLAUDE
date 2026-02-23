"""
Brave Search API Utility
Provides real-time web search capabilities using the Brave Search API.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def brave_search(query: str, count: int = 5) -> str:
    """
    Search the web using the Brave Search API.

    Args:
        query: The search query string
        count: Number of results to return (default: 5)

    Returns:
        Formatted string of search results with titles, descriptions, and URLs.
        Falls back to an error message if the API key is missing or request fails.
    """
    #api_key = os.environ.get("BRAVE_API_KEY", "")
    api_key = "BSA1AK6ycGp-9FJS5Q0k3a7qIZ39-Q7"

    if not api_key:
        return (
            "[WARNING: BRAVE_API_KEY not set in .env — real-time search unavailable.]\n"
            f"Query attempted: {query}"
        )

    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key,
    }
    params = {
        "q": query,
        "count": count,
        "search_lang": "en",
        "result_filter": "web",
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            web_results = data.get("web", {}).get("results", [])

            if not web_results:
                return f"No results found for: {query}"

            formatted = []
            for r in web_results:
                title = r.get("title", "No title")
                description = r.get("description", "No description available.")
                result_url = r.get("url", "")
                formatted.append(f"**{title}**\n{description}\nSource: {result_url}")

            return "\n\n---\n\n".join(formatted)

        elif response.status_code == 401:
            return "Brave Search API error: Invalid or expired API key (HTTP 401)."
        elif response.status_code == 429:
            return "Brave Search API error: Rate limit exceeded (HTTP 429). Try again later."
        else:
            return f"Brave Search API error: HTTP {response.status_code}"

    except requests.exceptions.Timeout:
        return "Brave Search request timed out after 10 seconds."
    except requests.exceptions.ConnectionError:
        return "Brave Search connection error. Check your internet connection."
    except requests.exceptions.RequestException as e:
        return f"Brave Search request failed: {str(e)}"
