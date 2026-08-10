import logging
from src.agents.equipment_resolver import EquipementResolver
from logger import setup_logger
from utils.llm_service import LLMService


setup_logger()

logger = logging.getLogger(__name__)


def main():
    llm = LLMService()
    resolver=EquipementResolver(llm_service=llm,)
    response = resolver.resolve("reactor")

    print(response)


if __name__ == "__main__":
    main()