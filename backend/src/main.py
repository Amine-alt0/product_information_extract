import logging
from logger import setup_logger
from utils.llm_service import LLMService
from src.agents.equipment_resolver import EquipementResolver
from src.agents.router_entity_status import RouterEntityType
from src.agents.validator_equipment import ValidatorEquipment
from src.agents.orchestrator import process_equipment
from utils.tavily_search_provider import TavilySearch
from src.agents.checker import check
from utils.utility_funcs import PipelineCache   # adjust path to wherever you saved it


def main():
    llm_service = LLMService()
    tavily = TavilySearch()
    cache = PipelineCache()

    resolver = EquipementResolver(llm_service)
    router = RouterEntityType()
    validator = ValidatorEquipment(tavily, llm_service)

    result = process_equipment(" machine MR34 Slicing", resolver, router, validator,tavily,llm_service,"none",cache,False)
    print(result)
    

if __name__ == "__main__":
    main()