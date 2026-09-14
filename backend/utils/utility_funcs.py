import os
import logging
from src.agents.equipment_resolver import Equipemenentity

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
        blocks.append(
            f"[{i}] {r.get('title', '')}\n"
            f"URL : {r.get('url', '')}\n"
            f"Extrait : {r.get('content', '')}\n"
        )
    return "\n".join(blocks)