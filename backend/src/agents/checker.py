import os 
import logging
import json
from src.agents.equipment_resolver import EquipementResolver
from src.agents.router_entity_status import RouterEntityType
from src.agents.validator_equipment import ValidatorEquipment
from src.agents.equipment_resolver import Equipemenentity
from utils.tavily_search_provider import TavilySearch
from utils.llm_service import LLMService
from utils.utility_funcs import build_search_query,merge_sources,hint_chooser,format_search_results


logger=logging.getLogger(__name__)

def check(results: dict) -> str:
    missing = []

    if not results.get("usage"):
        missing.append("l'usage de l'équipement")

    if not results.get("prix", {}).get("valeurs_observees"):
        missing.append("les informations de prix")

    if len(results.get("caracteristiques_techniques", [])) < 3:
        missing.append("davantage de caractéristiques techniques")

    return ", ".join(missing)