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

logger=logging.getLogger(__name__)


        
def run_specific_research( entity: Equipemenentity, sources:list[dict], tavily_search:TavilySearch,llm:LLMService)->list[dict]:
    query=build_search_query(entity,"la fiche technique de ")
    results=tavily_search.search(query=query,search_depth="advanced")
    sources.extend(results)
    
    price_results=discovery_search(entity,"price",llm,tavily_search)
    sources=merge_sources(sources,price_results)
    
    return sources
    