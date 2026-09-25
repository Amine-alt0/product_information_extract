import os
import logging
import json
from src.agents.equipment_resolver import Equipemenentity,EquipementResolver
from utils.tavily_search_provider import TavilySearch
from utils.utility_funcs import format_search_results,build_general_query,hint_chooser
from utils.llm_service import LLMService
from src.agents.shared_mechanism_search import discovery_search


logger=logging.getLogger(__name__)
     
GENERAL_EXTRACTION_PROMPT = """Tu es un assistant qui extrait des informations techniques et commerciales générales à partir de sources web, pour un TYPE d'équipement — aucun fabricant ni modèle spécifique n'a pu être identifié avec certitude.

Type d'équipement décrit :
- Catégorie : {category}
- Sous-catégorie : {subcategory}

IMPORTANT : les informations suivantes ne concernent PAS un produit unique et identifié, mais une CATÉGORIE d'équipements. Les sources rassemblées peuvent provenir de plusieurs fabricants et modèles différents correspondant à ce type d'équipement. Tu dois présenter les informations comme des valeurs TYPIQUES ou OBSERVÉES pour ce type d'équipement, jamais comme les caractéristiques d'un produit unique.

{hint_instruction}

Voici les sources rassemblées :

{sources_formatted}

À partir de ces sources UNIQUEMENT, extrait les informations suivantes.

Réponds STRICTEMENT en JSON, sans aucun texte avant ou après, avec ce format exact :
{{
  "usage": "description en français de l'utilisation/fonction typique de ce type d'équipement, ou null si non trouvée",
  "caracteristiques_techniques": [
    {{"nom": "nom de la caractéristique en français", "valeur": "valeur ou fourchette observée, avec unité", "source": "domaine de la source"}}
  ],
  "prix": {{
    "valeurs_observees": ["fourchette ou valeur par devise, ex: EUR: 100-300 €"],
    "sources": ["domaine1", "domaine2"],
    "note": "note en français sur la variabilité des prix selon fabricant/modèle/région, ou null"
  }},
  "sources": [
    {{"url": "url complète", "type": "fabricant" ou "distributeur" ou "document_technique" ou "autre"}}
  ],
  "notes": "note OBLIGATOIRE en français rappelant que ces informations décrivent un TYPE d'équipement correspondant à la description fournie, et non un produit unique et identifié ; précise aussi toute variation notable observée entre les sources (fabricants, modèles, régions)"
}}

Règles :
- N'invente aucune information absente des sources fournies.
- Pour chaque caractéristique, si les sources montrent des valeurs différentes selon le fabricant/modèle, présente une FOURCHETTE (ex: "0,5 à 5 kW") plutôt qu'une seule valeur, ou liste les valeurs typiques observées.
- Chaque caractéristique technique doit indiquer sa source (le domaine).
- Pour le prix : si plusieurs devises apparaissent, regroupe les valeurs PAR DEVISE (ex: ["EUR: 150-400 €", "USD: 100-350 $"]) plutôt que de tout mélanger dans une seule liste. Ne convertis jamais les devises toi-même.
- Si deux prix représentent la même valeur avec une notation de devise différente (ex: "₹" et "Rs"), ne les compte qu'UNE SEULE FOIS.
- Classe chaque source selon son type : "fabricant", "distributeur", "document_technique", ou "autre".
- Le champ "notes" NE PEUT JAMAIS être vide ou null pour cette extraction — il doit toujours rappeler qu'il s'agit d'un type d'équipement, pas d'un produit unique identifié.
- Toutes les valeurs textuelles doivent être en français, sauf les noms de marque/modèle mentionnés dans les sources qui restent dans leur forme officielle.
"""


def extract_general_infos(entity: Equipemenentity, sources: list[dict], llm: LLMService, hints: str) -> dict:
    formated_sources=format_search_results(sources)
    prompt=GENERAL_EXTRACTION_PROMPT.format(
        category=entity.category or "inconnu",
        subcategory=entity.subcategory or "inconnu",
        sources_formatted=formated_sources,
        hint_instruction=hint_chooser(hints)
        
    )
    logger.info(" making the extractrion of the general infos ")
    response=llm.invoke(prompt)
    fallback = {
            "usage": None,
            "caracteristiques_techniques": [],
            "prix": {"valeurs_observees": [], "sources": [], "note": None},
            "sources": [],
            "notes": "Échec de l'extraction — réponse invalide du LLM",
        }
    if not response or not response.strip():
        logger.warning("Empty response from LLM during domain filtering")
        return fallback
    
    try:
        parsed = json.loads(response)
    except json.JSONDecodeError:
        logger.warning("Failed to parse domain filter response: %s", response)
        return fallback
        
    return parsed
    