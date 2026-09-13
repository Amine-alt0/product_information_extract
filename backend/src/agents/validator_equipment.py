import os 
import logging
from pydantic import BaseModel
from logger import setup_logger
from utils.llm_service import LLMService
import json
from src.agents.equipment_resolver import EquipementResolver,Equipemenentity
from utils.tavily_search_provider import TavilySearch
from utils.llm_service import LLMService
from utils.formatting_results import format_search_results

logger=logging.getLogger(__name__)

VALIDATION_PROMPT = """Tu es un assistant qui aide à valider l'identité d'un équipement industriel.

Voici les informations partielles extraites automatiquement :
- Modèle : {model}
- Fabricant : {manufacturer}
- Catégorie : {category}
- Sous-catégorie : {subcategory}

Voici les résultats d'une recherche web effectuée pour vérifier ces informations :

{search_results}

En te basant UNIQUEMENT sur les résultats ci-dessus, détermine si ces informations correspondent à un produit spécifique et identifiable.

Réponds STRICTEMENT en JSON, sans aucun texte avant ou après, avec ce format exact :
{{
  "status": "VALID" ou "INVALID" ou "STILL_UNCERTAIN",
  "manufacturer": "nom du fabricant confirmé, ou null",
  "model": "modèle confirmé, ou null",
  "justification": "courte explication en une phrase"
}}

Règles :
- "VALID" seulement si les résultats confirment clairement un produit réel et identifiable.
- "INVALID" si les résultats montrent que ce n'est probablement pas un produit réel ou spécifique.
- "STILL_UNCERTAIN" si les résultats sont ambigus, contradictoires, ou insuffisants pour trancher.
- N'invente aucune information absente des résultats.
"""

class ValidationResult(BaseModel):
    status: str  # "VALID" | "INVALID" | "STILL_UNCERTAIN"
    updated_entity: Equipemenentity | None
    evidence_sources: list[dict]  # the Tavily results, kept for reuse
    
class ValidatorEquipment:
    def __init__(self,tavily_search,llm_service):
        self.tavily_search=tavily_search
        self.llm_service=llm_service
        pass
    def build_validation_query(self,entity: EquipementResolver) -> str:
        parts = []

        anchor = entity.model or entity.manufacturer or entity.normalized_name
        if anchor:
            parts.append(anchor)

        if entity.manufacturer and entity.manufacturer not in (anchor or ""):
            parts.append(entity.manufacturer)

        if entity.category:
            parts.append(entity.category)

        parts.append("manufacturer specifications")

        return " ".join(parts)
    
    def validate(self,entity:EquipementResolver)->dict:
        logger.info(
            " cheking the results... "
        )
        query=self.build_validation_query(entity)
        result=self.tavily_search.search(query)
        
        
        prompt = VALIDATION_PROMPT.format(
            model=entity.model or "inconnu",
            manufacturer=entity.manufacturer or "inconnu",
            category=entity.category or "inconnu",
            subcategory=entity.subcategory or "inconnu",
            search_results=self.format_search_results(result),
        )
        
        response=self.llm_service.invoke(prompt)
        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            logger.warning("Failed to parse validator response: %s", response)
            return {"status": "STILL_UNCERTAIN", "manufacturer": None, "model": None,
                    "justification": "Réponse invalide du LLM", "sources": result}

        return {
            "status": parsed["status"],
            "manufacturer": parsed.get("manufacturer"),
            "model": parsed.get("model"),
            "justification": parsed.get("justification"),
            "sources": result,
        }
        
        
        
        