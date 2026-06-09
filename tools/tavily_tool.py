from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None



def tavily_search(query):
    if client is None:
        return "Tavily search is unavailable because TAVILY_API_KEY is not set."

    try:
        response = client.search(query=query, max_results=5)
    except Exception as exc:
        return f"Tavily search failed: {exc}"

    results = []

    for i, r in enumerate(response.get("results", []), 1):
        title   = r.get("title", "Unknown")
        url     = r.get("url", "")
        snippet = r.get("content", "").strip()
        # Keep only the first 300 characters to avoid wall-of-text
        if len(snippet) > 300:
            snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

        results.append(f"{i}. **{title}**\n   {url}\n   {snippet}")

    return "\n\n".join(results) if results else "No Tavily results found."
    
    
    
