import os 
import logging
import json
from src.agents.equipment_resolver import EquipementResolver
from src.agents.router_entity_status import RouterEntityType
from src.agents.validator_equipment import ValidatorEquipment
from src.agents.equipment_resolver import Equipemenentity
from utils.tavily_search_provider import TavilySearch
from utils.llm_service import LLMService
from src.agents.specific_search import build_search_query
from utils.formatting_results import format_search_results

logger=logging.getLogger(__name__)


DOMAIN_FILTER_PROMPT = """Tu es un assistant qui évalue la pertinence de sources web pour la recherche {purpose_description}.

Voici le contexte de la recherche :
{context}

Voici les résultats d'une recherche web préliminaire :

{search_results}

Détermine lesquels de ces résultats sont des sources pertinentes et fiables pour {purpose_description} concernant cet équipement, par opposition à une source non pertinente (forum, article de blog générique, page sans rapport réel).

Réponds STRICTEMENT en JSON, sans aucun texte avant ou après, avec ce format exact :
{{
  "domains": ["domaine1.com", "domaine2.com"]
}}

Règles :
- N'inclus que le nom de domaine (ex: "grundfos.com"), jamais l'URL complète.
- N'inclus un domaine que s'il semble réellement pertinent et utile.
- Si aucun résultat n'est pertinent, renvoie une liste vide.
"""

def discovery_search(entity: Equipemenentity,purpose:str,llm:LLMService,tavily:TavilySearch)->list[dict]:
    if purpose=="price":
        input="le prix de "
        purposeofdescription = "d'informations sur le prix (marketplaces, distributeurs, fournisseurs)"
    else:
        input="la fiche technique de "
        purposeofdescription="de spécifications techniques (sites de fabricant, catalogues industriels, annuaires techniques)"
    discovery_query=build_search_query(entity,input)
    results=tavily.search(query=discovery_query,search_depth="basic")
    
    prompt=DOMAIN_FILTER_PROMPT.format(
        purpose_description=purposeofdescription,
        search_results=format_search_results(results),
        context = f"{entity.normalized_name or entity.category or ''}"
    )
    response=llm.invoke(prompt)
    if not response or not response.strip():
        logger.warning("Empty response from LLM during domain filtering")
        return results

    try:
        parsed = json.loads(response)
    except json.JSONDecodeError:
        logger.warning("Failed to parse domain filter response: %s", response)
        return results

    domains = parsed.get("domains", [])

    if not domains:
        return results

    final_result = tavily.search(
        query=discovery_query,
        search_depth="advanced",
        max_results=5,
        include_domains=domains,
    )
    return final_result
    
    