import logging
from src.agents.equipment_resolver import EquipementResolver
from logger import setup_logger
from utils.llm_service import LLMService


setup_logger()

logger = logging.getLogger(__name__)


from utils.tavily_search_provider import TavilySearch



def main():

    provider = TavilySearch()

    results = provider.search(
        "Grundfos CR 15-4 centrifugal pump specifications",
        max_results=5
    )

    for result in results:
        print("\nTITLE:", result.get("title"))
        print("URL:", result.get("url"))
        print("SCORE:", result.get("score"))
        print("CONTENT:", result.get("content", "")[:300])


if __name__ == "__main__":
    main()