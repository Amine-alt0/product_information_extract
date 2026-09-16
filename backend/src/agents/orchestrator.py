import os 
import logging
from src.agents.equipment_resolver import EquipementResolver
from src.agents.router_entity_status import RouterEntityType
from src.agents.validator_equipment import ValidatorEquipment
from src.agents.specific_search import run_specific_research
from utils.tavily_search_provider import TavilySearch
from utils.llm_service import LLMService
logger=logging.getLogger(__name__)



def process_equipment(name: str, resolver, router, validator, tavily:TavilySearch,llm:LLMService,hint:str):
    entity = resolver.resolve(name)
    decision = router.route(entity)

    if decision == "SPECIFIC":
        return run_specific_research(entity, sources=[], tavily_search=tavily,llm=llm,hints=hint)
    if decision == "UNCERTAIN":
        result = validator.validate(entity)

        if result["status"] == "VALID":
            entity.manufacturer = result["manufacturer"] or entity.manufacturer
            entity.model = result["model"] or entity.model
            return run_specific_research(entity, sources=[], tavily_search=tavily,llm=llm,hints=hint)
        else:
            return run_general_research(entity, sources=result["sources"])

    # decision == "GENERAL"
    return run_general_research(entity, sources=[])
            