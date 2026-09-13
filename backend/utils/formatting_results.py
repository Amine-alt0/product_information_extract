import os 

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