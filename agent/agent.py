from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.newspaper4k import Newspaper4k
from phi.tools.hackernews import HackerNews
from phi.tools.duckduckgo import DuckDuckGo


load_dotenv()

agent = Agent(
  model = Groq(id = 'llama-3.3-70b-versatile'),
  tools = [Newspaper4k(), DuckDuckGo(news = True,fixed_max_results=10), HackerNews(get_top_stories=True)],
  instructions = [
    "rewrite the article if it is biased"
    "use the tools to fecth the news if needed",
                 "Compare with different article and detect bias in the article and then rewrite the article bias free",
                  "Extract text if input is html but remember the html structure of article and when you rewrite the artcle write according to that html structure",
                  '''
                  Response should be json
                  Resnponse format=>{
                  "bias":"explain if it is biased article", 
                  "article":"the article to be rewritten"
                  }
                  '''
                 ]
)

if __name__ == "__main__":
  link = '''<html>
  <body>
  <div id = "main_content">
  Google is doing very good business. Very good company financially.
  </div>
  </body>
  </html>'''
  
  agent.print_response(f'rewrite if it is biased {link} max output word are 500')