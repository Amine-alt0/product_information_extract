import os 
import logging
from src.agents.equipment_resolver import EquipementResolver
from src.agents.router_entity_status import RouterEntityType
from src.agents.validator_equipment import ValidatorEquipment
from src.agents.equipment_resolver import Equipemenentity
from utils.tavily_search_provider import TavilySearch
from utils.llm_service import LLMService
from src.agents.shared_mechanism_search import discovery_search
from utils.utility_funcs import build_search_query,merge_sources
from src.agents.extract_specific_results import extract_specific_infos
from src.agents.checker import check
logger=logging.getLogger(__name__)


        
def run_specific_research( entity: Equipemenentity, sources:list[dict], tavily_search:TavilySearch,llm:LLMService,hints:str)->dict:
    query=build_search_query(entity,"la fiche technique de")
    results=tavily_search.search(query=query,search_depth="advanced")
    sources=merge_sources(sources,results)
    discovery_query=build_search_query(entity,"le prix de")
    price_results=discovery_search(entity,"price",llm,tavily_search,discovery_query)
    sources=merge_sources(sources,price_results)
    
    pre_results=extract_specific_infos(entity,sources,tavily_search,llm,hints)
    missing_text=check(pre_results)
    if missing_text:
        logger.info("we have a fall back here ")
        if "prix" in missing_text:
            new_query = build_search_query(entity, "le prix de ")
            new_results = discovery_search(entity, "price", llm, tavily_search,new_query)
            sources = merge_sources(sources, new_results)
        if "caractéristiques" in missing_text:
            new_query = build_search_query(entity, "la fiche technique de ")
            new_results = discovery_search(entity, "specs", llm, tavily_search,new_query)
            sources = merge_sources(sources, new_results)

        result = extract_specific_infos(entity, sources, tavily_search, llm, hints=missing_text)
        return result
    return pre_results
        
    