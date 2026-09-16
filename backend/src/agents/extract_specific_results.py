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

EXTRACTION_PROMPT = """Tu es un assistant qui extrait des informations techniques et commerciales structurées à partir de sources web, pour un équipement déjà identifié avec certitude.

Équipement identifié :
- Fabricant : {manufacturer}
- Modèle : {model}
- Nom normalisé : {normalized_name}
- Catégorie : {category}

{hint_instruction}

Voici les sources rassemblées à son sujet :

{sources_formatted}

À partir de ces sources UNIQUEMENT (même si tu connais des informations générales sur ce fabricant ou ce type d'équipement, n'utilise QUE les sources fournies), extrait les informations suivantes.

Réponds STRICTEMENT en JSON, sans aucun texte avant ou après, avec ce format exact :
{{
  "usage": "description en français de l'utilisation/fonction de cet équipement, ou null si non trouvée",
  "caracteristiques_techniques": [
    {{"nom": "nom de la caractéristique en français", "valeur": "valeur avec unité", "source": "domaine de la source"}}
  ],
  "prix": {{
    "valeurs_observees": ["valeur1", "valeur2"],
    "sources": ["domaine1", "domaine2"],
    "note": "courte note en français sur la fiabilité/variabilité du prix, ou null"
  }},
  "sources": [
    {{"url": "url complète", "type": "fabricant" ou "distributeur" ou "document_technique" ou "autre"}}
  ],
  "notes": "note en français sur toute incertitude, incohérence entre sources, ou correspondance imparfaite avec l'équipement identifié ; chaîne vide si aucune"
}}

Règles :
- N'invente aucune information absente des sources fournies.
- Chaque caractéristique technique doit indiquer sa source (le domaine, ex: "grundfos.com").
- Pour le prix, si plusieurs valeurs différentes apparaissent dans les sources, liste-les TOUTES dans "valeurs_observees" plutôt que d'en choisir une seule ou de faire une moyenne.
- IMPORTANT — avant d'inclure un prix, vérifie qu'il correspond bien au modèle exact identifié ({model}) :
  - Si une source de prix concerne une variante différente (tension, phase électrique, type de connexion, région) du même modèle de base, tu PEUX l'inclure mais DOIS le signaler dans "notes" (ex : "prix observé pour une variante 60Hz/monophasé, non pour la version exacte identifiée").
  - Si une source de prix concerne un modèle différent de la même famille (ex : CRE au lieu de CR, un numéro de modèle différent), NE L'INCLUS PAS dans "valeurs_observees" — mentionne-le dans "notes" à la place.
  - Si une source de prix concerne un accessoire, une pièce détachée, ou un kit (ex : "stack kit", "chamber kit"), et non l'équipement complet, NE L'INCLUS PAS dans "valeurs_observees" — mentionne-le dans "notes" à la place.
- Si aucune information de prix fiable n'est trouvée, renvoie "valeurs_observees": [] et "sources": [], et explique pourquoi dans "notes" si des prix ont été rejetés.
- Classe chaque source selon son type : "fabricant", "distributeur", "document_technique", ou "autre".
- Si une source semble décrire une variante légèrement différente du modèle exact, mentionne-le dans "notes".
- Toutes les valeurs textuelles doivent être en français, sauf les noms de marque/modèle qui restent dans leur forme officielle.
- Si plusieurs prix sont exprimés dans des devises différentes, NE LES CONVERTIS PAS toi-même ; indique clairement la devise pour chaque valeur (ex: "245,00 €" et non juste "245").
- Si deux valeurs représentent le même prix mais avec une notation de devise différente (ex: "₹" et "Rs" pour la roupie indienne), ne les compte qu'UNE SEULE FOIS.
- Si les prix couvrent plusieurs devises très différentes, regroupe-les par devise dans "valeurs_observees" plutôt que de les lister en vrac (ex: ["EUR: 122,50–245,00 €", "USD: 90,00–190,00 $", "INR: 12 500,00 ₹"]).
"""

def extract_specific_infos(entity:Equipemenentity,sources:list[dict],tavily:TavilySearch,llm:LLMService,hints:str)->dict:
    results=format_search_results(sources)
    prompt=EXTRACTION_PROMPT.format(
        manufacturer = entity.manufacturer or "inconnu",
        model = entity.model or "inconnu",
        normalized_name = entity.normalized_name or "inconnu",
        category = entity.category or "inconnu",
        hint_instruction=hint_chooser(hints),
        sources_formatted=results,
    )
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
    
    
