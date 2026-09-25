import os
import logging
import json
from datetime import datetime
from src.agents.equipment_resolver import Equipemenentity

logger = logging.getLogger(__name__)

def merge_sources(existing: list[dict], new: list[dict]) -> list[dict]:
    seen_urls = {s.get("url") for s in existing}
    for item in new:
        if item.get("url") not in seen_urls:
            existing.append(item)
            seen_urls.add(item.get("url"))
    return existing

def build_search_query( entity: Equipemenentity,input: str)-> str:
    extracted_query= []
    extracted_query.append(input)
    if entity.normalized_name is not None:
        extracted_query.append(entity.normalized_name)
    else:
        if entity.manufacturer is not None :
            extracted_query.append(entity.manufacturer)
        if entity.model is not None:
            extracted_query.append(entity.model)
    return " ".join(extracted_query)
def hint_chooser(input:str)-> str:
    if input:
        hint_instruction = "Priorise ces informations : " + input
    else:
        hint_instruction = "Décide toi-même quelles sont les informations les plus importantes à mettre en avant."
    return hint_instruction
def format_search_results(results: list[dict]) -> str:
    if not results:
        return "Aucun résultat trouvé."

    blocks = []
    for i, r in enumerate(results, start=1):
        text = r.get("raw_content") or r.get("content", "")
        blocks.append(
            f"[{i}] {r.get('title', '')}\n"
            f"URL : {r.get('url', '')}\n"
            f"Extrait : {r.get('content', '')}\n"
        )
    return "\n".join(blocks)
def build_general_query(entity:Equipemenentity,input:str)->str:
    extracted_query = [input]

    if entity.normalized_name:
        extracted_query.append(entity.normalized_name)
    else:
        if entity.manufacturer:
            extracted_query.append(entity.manufacturer)
        if entity.model:
            extracted_query.append(entity.model)

    if entity.category:
        extracted_query.append(entity.category)
    if entity.subcategory:
        extracted_query.append(entity.subcategory)

    return " ".join(extracted_query)

class PipelineCache:
    def __init__(self, filepath: str = "equipment_cache.json"):
        self.filepath = filepath
        self.data = self._load()

    def _load(self) -> dict:
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning("Failed to load cache file (%s), starting fresh: %s", self.filepath, e)
            return {}

    def _save(self) -> None:
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except OSError as e:
            logger.warning("Failed to save cache file (%s): %s", self.filepath, e)

    def normalize_key(self, name: str) -> str:
        return name.strip().lower()

    def get(self, name: str) -> dict | None:
        key = self.normalize_key(name)
        entry = self.data.get(key)
        if entry:
            logger.info("Cache hit for equipment: %s", name)
        else:
            logger.info("Cache miss for equipment: %s", name)
        return entry

    def set(self, name: str, result: dict, decision: str) -> None:
        key = self.normalize_key(name)
        self.data[key] = {
            "result": result,
            "decision": decision,
            "cached_at": datetime.now().isoformat(),
        }
        self._save()
        
        
