from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.document_loaders import NewsURLLoader
import json
import re
import requests
from bs4 import BeautifulSoup

wrapper = DuckDuckGoSearchAPIWrapper(max_results=5)

# Updated search function to take a dynamic query
def search_similar_articles(query):
    search = DuckDuckGoSearchResults(api_wrapper=wrapper)
    return search.invoke(query)

# Corrected Tool definition
search_similar_articles_tool = Tool(
    name="search_similar_articles_tool",
    func=search_similar_articles,
    description="use this tool to Searches= for similar articles from the web."
)
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
    description="Load and extract news articles from given URL. if input is not url dont use this tool"
    
)
def fallback_article_fetcher(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        
        body_text = soup.body.get_text(separator=' ', strip=True) if soup.body else ''

        
        return body_text

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
 

def processThought(thought):
  return thought

processThought_tool= Tool(
    name= "Thought Processing",
    description= """This is useful for when you have a thought that you want to use in a task, 
    but you want to make sure it's formatted correctly. 
    Input is your thought and self-critique and output is the processed thought""",
    func= processThought
  )
  
  