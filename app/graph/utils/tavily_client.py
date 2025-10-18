import os
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=api_key)