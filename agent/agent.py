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

If provided input is not url you do no need to use article_loader or fallback article loader, 
If only provided input is url then use article_loader or fallback artcle loader tools.
If the primary article fetching method fails, use the `fallback_article_loader` tool.
Rely on earch_similar_articles_tool to gather similar articles and compare them.

you dont need any tool to write the "content" html. you do it with your own knowledge and reasoning.
if you are having json format error or missing action after though just return the text in thought. I will handle rest.


Format your response like this:
```json
{{
    "bias": "Detailed explanation of the identified bias (if any).",
    "content": "The rewritten, bias-free version of the article formatted in styled HTML."
}}
```

"""






llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.3)

agent = initialize_agent(
    tools=[search_similar_articles_tool, news_loader_tool,fallback_news_loader_tool],
    llm=llm,
    verbose=not PROD,
    handle_parsing_errors=True,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
)

def bias_checker(query):
    prompt = template.format(query = query)
    res = agent.invoke(prompt)
    print(res)
    ans= parse_agent_response(res["output"])
    print(ans)
    # ans= parse_agent_response(res)
    
    return ans



if __name__ == "__main__":
    link ="https://www.hindustantimes.com/world-news/us-news/spacex-crew-9-back-on-earth-what-nasa-astronauts-sunita-williams-butch-wilmore-ate-and-did-for-9-months-101742344002095.html"

    res = bias_checker(link)
    print(res)


