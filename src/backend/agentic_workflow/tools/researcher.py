import os
from typing import List

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from chat.config import Config


def tavily_tool(config: Config):
    os.environ["TAVILY_API_KEY"] = config.get_tavily_api_key()
    return TavilySearchResults(max_results=1)


@tool
def scrape_webpages(urls: List[str]) -> str:
    """Use requests and bs4 to scrape the provided web pages for detailed information."""
    loader = WebBaseLoader(urls)
    docs = loader.load()
    return "\n\n".join(
        [
            f'<Document name="{doc.metadata.get("title", "")}">\n{doc.page_content[:5000]}\n</Document>'
            for doc in docs
        ]
    )
