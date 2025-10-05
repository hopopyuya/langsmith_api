from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
import requests
import tweepy
import os

## APIキー
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET_KEY = os.getenv("X_API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

## LangSmithの設定
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_PROJECT"] = "news-twitter-agent"


# NewsAPIでニュースを最新のニュースを1個取得するTool
@tool
def get_news(query: str) -> str:
    """キーワードに合致する最新ニュースを1件取得しタイトルと説明を返す"""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "sortBy": "publishedAt",
        "pageSize": 1,
        "apiKey": NEWS_API_KEY,
    }
    article = requests.get(url, params).json()["articles"][0]
    return f"{article['title']} - {article['description']}"


# 140字以内で要約するTool
@tool
def summarize(text: str) -> str:
    """テキストを要約して返す"""
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3, openai_api_key=OPENAI_API_KEY)
    return llm.invoke(
        [
            SystemMessage(content="提供されたテキストを140文字以内に要約してください"),
            HumanMessage(content=text),
        ]
    ).content


# TweetをするTool
@tool
def post_tweet(text: str) -> str:
    """テキストをTweetする"""
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET_KEY,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )
    tweet = client.create_tweet(text=text)
    return f"{tweet.data['id']}"


def decide_next(state: MessagesState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools_edge"
    return "end"


def call_llm(state: MessagesState) -> str:
    system_prompt = "ユーザーの入力に応じて、get_newsとsummarizeとpost_tweetから適切なツールを使って処理をおこなってください"
    messages = state["messages"]
    if not any(isinstance(msg, SystemMessage) for msg in messages):
        messages = [SystemMessage(content=system_prompt)] + messages

    llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)
    response = llm.bind_tools([get_news, summarize, post_tweet]).invoke(messages)

    return {"messages": messages + [response]}


tools_node = ToolNode([get_news, summarize, post_tweet])

# Graph構築
graph = StateGraph(MessagesState)
graph.add_node("llm", call_llm)
graph.add_node("tools_node", tools_node)
graph.set_entry_point("llm")
graph.add_conditional_edges(
    "llm", decide_next, {"tools_edge": "tools_node", "end": "__end__"}
)
graph.add_edge("tools_node", "llm")

app = graph.compile()
