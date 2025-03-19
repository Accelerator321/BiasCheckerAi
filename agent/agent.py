from tools import *

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent
from dotenv import load_dotenv
import re
import os


load_dotenv()

PROD = int(os.getenv("PROD", 0))

template = """
You are an expert media analyst specialized in detecting and addressing bias in articles. 

Your task is to:
1. Analyze the provided article for bias. Identify any partiality, misleading language, or lack of neutrality.
2. Rewrite the article in a bias-free manner while preserving the factual content.
3. Search and compare similar articles to enhance the accuracy of your analysis. However, prioritize your own assessment over tool dependencies.
4. input may be a url or the article content itself. you have to be able to handle both.
5. use fallback_article_loader if article_loader fails
input: {query}
Format your response as a JSON object like this:
```json
{{
    "bias": "Detailed explanation of the identified bias (if any).",
    "content": "The rewritten, bias-free version of the article formatted in styled HTML."
}}
"""


llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.3)

agent = initialize_agent(
    tools=[web_search, news_loader_tool,fallback_news_loader_tool],
    llm=llm,
    verbose=not PROD,
    handle_parsing_errors=True,
)

def bias_checker(query):
    prompt = template.format(query = query)
    res = agent.invoke(prompt)
    ans= parse_agent_response(res["output"])
    print(ans)
    return ans



if __name__ == "__main__":
    link ="https://www.hindustantimes.com/world-news/us-news/spacex-crew-9-back-on-earth-what-nasa-astronauts-sunita-williams-butch-wilmore-ate-and-did-for-9-months-101742344002095.html"

    res = bias_checker(link)
    print(res)


