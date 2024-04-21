import os

import requests
from bs4 import BeautifulSoup
from langchain.agents import Tool,initialize_agent, AgentType
from langchain.tools import BaseTool
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI

import pyautogui as pyg
import webbrowser as web

os.environ["GOOGLE_API_KEY"] = "AIzaSyA8j9C2iflu3S-xFNg0KJfNSjeBpKvpzXY"

search = DuckDuckGoSearchRun()

tools = [
        Tool(
        name = "DuckDuckGo Search",
        func = search.invoke,
        description = "Useful when need to search on the internet."
    ), 
    
]

def GetMarketData(symbol: str, mins: int) -> dict:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={mins}&apikey=HDAOWX4BNZ81OHAL'

    r = requests.get(url)
    data = r.json()
    
    historical_data = data["Time Series (5min)"]
    
    return historical_data


from bs4 import BeautifulSoup
from langchain.tools import BaseTool


class BloombergMarketNews(BaseTool):
    name = "Bloomberg Market News"
    description = "Scrapes market news from Bloomberg for analysis."

    def _run(self, url: str):
        url = url
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            news_headlines = soup.find_all("h1", class_="headline")

            market_news = [headline.text for headline in news_headlines]

            return market_news
        else:
            return "Failed to retrieve market news from Bloomberg."

# Usage example
bloomberg_tool = BloombergMarketNews()

import time

class WebSeach:
    description = """
    1:This will open a the web page url you entered via the run function: like this one run("https://example.com" or even ".org", ".ai", ",io" and other domain names if they are needed)
    2: It will return a screenshot for the page every time you scroll up or down and save it as vaarible and turned into a pdf where you extractract the text directly.
    3: When the pdf is returned you read the extracted text as it is and you learn from that."""
    def _run(self, url):
        web.open_new_tab(url)
        time.sleep(5)
        page = pyg.screenshot()
        page
            

bloomberg_tool = Tool(
    name = "Bloomberg Market News",
    func= bloomberg_tool.run,
    description = bloomberg_tool.description 
)
tools.append(bloomberg_tool)

data_tool = Tool(
    name= "market_data_tool",
    description= "Fetches market data, including price (open, high, low, close) and volume, to facilitate trend identification.  just input the ticker you want to find e.g: `APPL` or `TSLA` etc. and you also use the mins params to choose the the time frames you want such as [5, 15, 30]" ,
    func= GetMarketData,
)

tools.append(data_tool)

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=.0)

tools.append(YahooFinanceNewsTool())

Agent = initialize_agent(tools,
                        llm,
                        Verbose=True,
                        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)