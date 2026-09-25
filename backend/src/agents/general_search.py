import os
import logging
import json
from src.agents.equipment_resolver import Equipemenentity,EquipementResolver
from utils.tavily_search_provider import TavilySearch
from utils.utility_funcs import format_search_results,build_general_query,merge_sources
from utils.llm_service import LLMService
from src.agents.shared_mechanism_search import discovery_search
from src.agents.extract_general_infos import extract_general_infos
from src.agents.checker import check

logger=logging.getLogger(__name__)
     


def run_general_search(entity:Equipemenentity,sources:list[dict],tavily:TavilySearch,llm:LLMService,hints:str)->dict:
    query_specs=build_general_query(entity,"la fiche technique de ")
    specs_sources=discovery_search(entity,"specs",llm,tavily,query_specs)
    query=build_general_query(entity,"le prix de ")
    price_sources=discovery_search(entity,"price",llm,tavily,query)
    
    discovery_results=merge_sources(sources,specs_sources)
    discovery_results=merge_sources(discovery_results,price_sources)
    
    pre_results=extract_general_infos(entity,discovery_results,llm,hints)
    missing_text=check(pre_results)
    if missing_text:
        logger.info("we have a fall back here ")
        sources=discovery_results
        if "prix" in missing_text:
            new_query = build_general_query(entity, "le prix de ")
            new_results = discovery_search(entity, "price", llm, tavily,new_query)
            sources = merge_sources(sources, new_results)
        if "caractéristiques" in missing_text:
            new_query = build_general_query(entity, "la fiche technique de ")
            new_results = discovery_search(entity, "specs", llm, tavily,new_query)
            sources = merge_sources(sources, new_results)

        results = extract_general_infos(entity, sources, llm, hints=missing_text)
        return results
    return pre_results
    
    
    
    
    