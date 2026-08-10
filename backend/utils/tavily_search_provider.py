import logging

from config import TAVILY_API_KEY
from tavily import TavilyClient


logger = logging.getLogger(__name__)


class TavilySearch:

    def __init__(self):
        self.api_key = TAVILY_API_KEY

        if not self.api_key:
            raise ValueError("TAVILY_API_KEY is not configured")

        self.client = TavilyClient(
            api_key=self.api_key
        )

        logger.info(
            "Tavily search provider initialized"
        )

    def search(
        self,
        query: str,
        search_depth: str = "basic",
        max_results: int = 5,
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        topic: str = "general",
        time_range: str | None = None,
    ):
        logger.info(
            "Searching Tavily: %s",
            query
        )

        response=self.client.search(
            query=query,
            search_depth=search_depth,
            max_results=max_results,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            topic=topic,
            time_range=time_range,
        )
        return response.get("results", [])