"""Search on the web with Tavily"""

import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv(override=True)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily = TavilyClient(api_key=TAVILY_API_KEY)

response = tavily.search("What is the latest news about AI?")

for result in response["results"]:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Content: {result['content']}\n")
