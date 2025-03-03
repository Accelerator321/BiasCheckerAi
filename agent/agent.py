from dotenv import load_dotenv
from phi.agent.agent import Agent
from phi.model.groq.groq import Groq
from phi.tools.newspaper4k import Newspaper4k
from phi.tools.hackernews import HackerNews
from phi.tools.duckduckgo import DuckDuckGo
from pydantic import BaseModel, Field
from phi.utils.pprint import pprint_run_response
import re

load_dotenv()

instructions = [
    "Rewrite the article if it is biased.",
    "Use the tools to fetch news if needed.",
    "Compare with different articles and detect bias before rewriting.",
    "Extract text and rewrite article return response in format instructed",
    '''Response format=>
    <bias>explain the biasness if any</bias>,
    <output>rewrite the article html bias free and also add write css in for good ui</output>
     ''',
    "It is strict instruction to write your response in the format told above xml format strictly"
]
description = "This agent checks if the article is biased and rewrites the bias free article with html. It has necessary tools to fetch news from link and fetching other related articles and also has a bias checker."

tools = [
    Newspaper4k(),
    DuckDuckGo(news=True, fixed_max_results=6),
    HackerNews(get_top_stories=True)
]
# first_agent = Agent(model=Groq(id='deepseek-r1-distill-llama-70b'),
#                     show_tool_calls=False,
#                     tools=tools,
#                     description=description,
#                     markdown=True,
#                     instructions=instructions,
#                     structured_outputs=False)

# second_agent = Agent(
#     model=Groq(id='gemma2-9b-it'),
#     show_tool_calls=False,
#     tools=tools,
#     description="",
#     markdown=True,
#     instructions=[
#         '''Response format=>
#                  <bias>explain the biasness if any</bias>,
#                  <output>rewrite the article html bias free and also add write css in for good ui</content>
#                   ''',
#         "It is strict instruction to write your response in the format told above xml format strictly"
#     ])

agent = Agent(
    model=Groq(id='deepseek-r1-distill-llama-70b'),
    tools=tools,
    description=description,
    # "This is the main it uses tools and also other team members to analyze the given article for bias and rewrite it bias free",
    markdown=True,
    instructions=instructions,
)


def check_bias(article, cnt=0):
    try:
        if cnt >= 5:
            return {"bais": "", "content": ""}
        res = agent.run(
            f"fetch the news from link Rewrite the article if it is biased: {article}.",
        )

        res = res.dict()
        res = res['content']

        bias = re.search(r'<bias>([\s\S]*?)</bias>', res, re.S).group(1)
        content = re.search(r'<output>([\s\S]*?)</output>', res, re.S).group(1)

        # print(res)
        # print("_____________\n")
        # print(
        #     bias,
        #     "\n\n",
        #     content,
        # )

        out = {"bias": "", "content": ""}

        if bias:
            out['bias'] = bias
        if content:
            out['content'] = content

        if not out["content"]: return check_bias(article, cnt + 1)
        return out
    except Exception as e:
        print(e)
        return check_bias(article, cnt + 1)


if __name__ == "__main__":
    link = 'https://www.hindustantimes.com/india-news/only-source-of-livelihood-ranveer-allahbadia-asks-sc-to-allow-him-to-upload-shows-101740992546533.html'

    print(check_bias(link))
