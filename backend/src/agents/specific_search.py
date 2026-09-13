import os 
import logging
from src.agents.equipment_resolver import EquipementResolver
from src.agents.router_entity_status import RouterEntityType
from src.agents.validator_equipment import ValidatorEquipment
from src.agents.equipment_resolver import Equipemenentity
from utils.tavily_search_provider import TavilySearch



logger=logging.getLogger(__name__)



def build_search_query( entity: Equipemenentity)-> str:
    extracted_query= []
    extracted_query.append("la fiche technique de ")
    if entity.manufacturer is not None :
        extracted_query.append(entity.manufacturer)
    if entity.model is not None:
        extracted_query.append(entity.model)
    return " ".join(extracted_query)
        
def run_specific_research( entity: Equipemenentity, sources:list[dict], tavily_search:TavilySearch)->list[dict]:
    query=build_search_query(entity)
    results=tavily_search.search(query=query,search_depth="advanced")
    sources.extend(results)
    return sources