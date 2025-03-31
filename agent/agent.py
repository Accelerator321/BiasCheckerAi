from tools import *


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent,AgentType
from dotenv import load_dotenv
import re
import os


load_dotenv()

PROD = int(os.getenv("PROD", 0))

template = """
according to instructions above analyze the articles for bias and rewrite it => {query}
Your task is to analyze the given input to identify any partiality, misleading language, or lack of neutrality.
First you need to fetch the article provided in user query
If provided input is not url you do no need to use news_loader_tool, 
If only provided input is url then use news_loader_tool.

Rely on get_news_links_tool to gather the url of the related articles for nearby date as the orginal article(given by user)(!important).

now load the fetched links and do comparison to do bias anlysis gather info for writing bias free article, 
Try to load artcles from atleast 3 diffrent sources(different domain also) first.
you dont need any tool to write the "content" html. you do it with your own knowledge and reasoning.
if you are having json format error or missing action after though just return the text in thought. I will handle rest.


Format your response like this:
```json
{{
    "bias": "Detailed explanation of the identified bias (if any).",
    "content": "The rewritten, bias-free version of the article formatted in styled HTML. 
                include the soruces of related articles in html"
}}
```

"""






llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.3)

agent = initialize_agent(
    tools=[get_news_links_tool, news_loader_tool],
    llm=llm,
    verbose=not PROD,
    handle_parsing_errors=True,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    max_iterations = 20
)

def bias_checker(query):
    prompt = template.format(query = query)
    res = agent.invoke(prompt)
    ans = res["output"]

    
    return ans



if __name__ == "__main__":
    link ="https://www.bbc.com/news/articles/cx278d4702xo"

    res = bias_checker(link)
    


