import os
import logging
from src.agents.equipment_resolver import Equipemenentity,EquipementResolver
from utils.tavily_search_provider import TavilySearch
from validator_equipment import format_search_result
logger=logging.getLogger(__name__)
from utils.formatting_results import format_search_result
from utils.tavily_search_provider import TavilySearch
from utils.llm_service import LLMService


class GeneralSearch:
    def __init__(self,tavily_search,llm_service,entity:Equipemenentity):
        self.tavily_search=tavily_search
        self.llm_service=llm_service
        
    def build_gsearch_query(self, entity, purpose:str)->str:
        parts = []
        
        if entity.model:
            parts.append(entity.model)
        if entity.manufacturer :
             parts.append(entity.manufacturer)
        if entity.category:
            parts.append(entity.category)
        if entity.subcategory:
            parts.append(entity.subcategory)
        if purpose=="specs":
            parts.append("spécifications techniques")
        elif purpose=="price":
            parts.append("prix fournisseur")
        
        return " ".join(parts)
    def open_tavily_search(self,entity,purpose,quey,tavily_search)->list[dict]:
        query=self.build_gsearch_query(entity,purpose)
        results=tavily_search.search(query)
        
        