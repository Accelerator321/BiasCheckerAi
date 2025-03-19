from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.document_loaders import NewsURLLoader
import json
import re
import requests
from bs4 import BeautifulSoup

wrapper = DuckDuckGoSearchAPIWrapper(max_results=4)

web_search = DuckDuckGoSearchResults(api_wrapper=wrapper, source="news")

def load_news_articles(url):
    try:
        loader = NewsURLLoader([url])
        docs = loader.load()
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return "Could not fetch"

news_loader_tool = Tool(
    name = "article_loader",
    func=load_news_articles,
    description="Load and extract news articles from given URL"
    
)
def fallback_article_fetcher(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        
        body_text = soup.body.get_text(separator=' ', strip=True) if soup.body else ''

        
        return body_text[:8000]

    except Exception as e:
        return f"Error fetching the article"


fallback_news_loader_tool = Tool(
    name = "fallback_news_loader_tool",
    func=fallback_article_fetcher,
    description="Fetches the plain inner text of a URL if the primary article_loader tool fails."
)

def parse_agent_response(response):
    pattern = r'```json\s*([\s\S]*?)\s*```'

  
    match = re.search(pattern, response)
    ans = {}
    if match:
        json_content = match.group(1)
        try:
            parsed_json = json.loads(json_content)
            ans = parsed_json
        except json.JSONDecodeError:
            ans = {}
    else:
        print("No JSON found")
    return ans
