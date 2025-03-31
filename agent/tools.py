from langchain.tools import Tool, tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.document_loaders import NewsURLLoader
import json
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json5
from pydantic import BaseModel
from langchain.tools import StructuredTool

wrapper = DuckDuckGoSearchAPIWrapper(max_results=5)
search = DuckDuckGoSearchResults(api_wrapper=wrapper)

def search_similar_articles(query):
    return search.invoke(query)

search_similar_articles_tool = Tool(
    name="search_similar_articles_tool",
    func=search_similar_articles,
    description="use this tool to Searches= for similar articles from the web."
)

def selenium_article_fetcher(url, driver):
    try:
        driver.get(url)
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup.body.get_text(separator=' ', strip=True) if soup.body else ''
    except Exception as e:
        return f"Error fetching the article: {str(e)}"

def load_news_articles(url, driver):
    try:
        loader = NewsURLLoader([url])
        docs = loader.load()
        if not docs or not docs[0]: raise Exception("Something went wrong!")
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception:
        return selenium_article_fetcher(url, driver)

news_loader_tool = Tool(
    name="article_loader",
    func=lambda url: load_news_articles(url, driver),
    description="Load and extract news articles from given URL. if input is not url dont use this tool"
)

def parse_agent_response(response):
    try:
        return json.loads(response, strict=False)
    except:
        try:
            return json5.loads(response)
        except:
            match = re.search(r'```json\s*([\s\S]*?)\s*```', response)
            return json.loads(match.group(1), strict=False) if match else {}

def processThought(thought):
    return thought

processThought_tool = Tool(
    name="Thought Processing",
    description="This is useful for when you have a thought that you want to use in a task, but you want to make sure it's formatted correctly. Input is your thought and self-critique and output is the processed thought",
    func=processThought
)

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_news_links(topic: str, date: str):
    if not topic:
        return "Topic not detected, please try again."
    if not date:
        return "Invalid date format (YYYY-MM-DD expected)."

    sources = ["cnn.com", "bbc.com", "nytimes.com", "washingtonpost.com", "foxnews.com", "nbcnews.com"]
    query = f"{topic} after:{date} before:{date} " + " OR ".join([f"site:{src}" for src in sources])
    search_url = f"https://www.google.com/search?q={query}&tbm=nws"

    driver.get(search_url)
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.WlydOe")))
        links = [article.get_attribute("href") for article in driver.find_elements(By.CSS_SELECTOR, "a.WlydOe") if article.get_attribute("href")]
    except Exception as e:
        links = [f"Error: {str(e)}"]
    return links

class NewsSearchInput(BaseModel):
    topic: str
    date: str

get_news_links_tool = StructuredTool.from_function(
    get_news_links,
    name="get_news_links",
    description="Fetch news articles for a given topic and date.",
    args_schema=NewsSearchInput
)

if __name__ == "__main__":
    query = json.dumps({"topic": "Donald Trump", "date": "2025-03-31"})
    print(get_news_links("Donald Trump", "2025-03-31"))