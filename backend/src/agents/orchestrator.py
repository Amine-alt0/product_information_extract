import os 
import logging
from src.agents.specific_search import run_specific_research
from utils.tavily_search_provider import TavilySearch
from utils.llm_service import LLMService
from src.agents.general_search import run_general_search
logger=logging.getLogger(__name__)



def process_equipment(name: str, resolver, router, validator, tavily:TavilySearch,llm:LLMService,hint:str,cache, force_refresh=False):
    if not force_refresh:
        cached = cache.get(name)
        if cached:
            return cached["result"]
        
    entity = resolver.resolve(name)
    decision = router.route(entity)

    if decision == "SPECIFIC":
        result=run_specific_research(entity, sources=[], tavily_search=tavily,llm=llm,hints=hint)
        cache.set(name, result, decision)
        return result
    if decision == "UNCERTAIN":
        result = validator.validate(entity)

        if result["status"] == "VALID":
            entity.manufacturer = result["manufacturer"] or entity.manufacturer
            entity.model = result["model"] or entity.model
            result=run_specific_research(entity, sources=result["sources"], tavily_search=tavily,llm=llm,hints=hint)
            cache.set(name, result, decision)
            return result
        else:
            result=run_general_search(entity, sources=result["sources"],tavily=tavily,llm=llm,hints=hint)
            cache.set(name, result, decision)
            return result

    # decision == "GENERAL"
    result=run_general_search(entity, sources=[],tavily=tavily,llm=llm,hints=hint)
    cache.set(name, result, decision)
    return result
            