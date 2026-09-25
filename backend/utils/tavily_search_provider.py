import logging

from config import TAVILY_API_KEY
from tavily import TavilyClient


logger = logging.getLogger(__name__)


class TavilySearch:

    def __init__(self):
        self.api_key = TAVILY_API_KEY
        self._cache={}
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY is not configured")

        self.client = TavilyClient(
            api_key=self.api_key
        )

        logger.info(
            "Tavily search provider initialized"
        )
    def build_cache_key(self, query, search_depth, max_results, include_domains, exclude_domains, topic, time_range,include_raw_content):
        return (
        query,
        search_depth,
        max_results,
        tuple(sorted(include_domains)) if include_domains else None,
        tuple(sorted(exclude_domains)) if exclude_domains else None,
        topic,
        time_range,
        include_raw_content,
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
        include_raw_content: str | bool = "markdown"
    ):  
        key=self.build_cache_key(query, search_depth, max_results, include_domains, exclude_domains, topic, time_range,include_raw_content)
        logger.info(
            "Searching Tavily: %s ",
            query
        )
        if key in self._cache:
            return self._cache[key]
        response=self.client.search(
            query=query,
            search_depth=search_depth,
            max_results=max_results,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            topic=topic,
            time_range=time_range,
            include_raw_content=include_raw_content,
        )
        self._cache[key]=response.get("resultst" , [])
        return response.get("results", [])