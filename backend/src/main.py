import logging
from logger import setup_logger
from utils.llm_service import LLMService
from src.agents.equipment_resolver import EquipementResolver
from src.agents.router_entity_status import RouterEntityType
from src.agents.validator_equipment import ValidatorEquipment
from src.agents.orchestrator import process_equipment
from utils.tavily_search_provider import TavilySearch

def main():
    llm_service = LLMService()
    tavily = TavilySearch()

    resolver = EquipementResolver(llm_service)
    router = RouterEntityType()
    validator = ValidatorEquipment(tavily, llm_service)

    result = process_equipment("Grundfos CR 15-4", resolver, router, validator,tavily,llm_service)
    print(result)

if __name__ == "__main__":
    main()