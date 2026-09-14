from flask import Flask, request, render_template_string
import json

from src.agents.equipment_resolver import EquipementResolver
from src.agents.router_entity_status import RouterEntityType
from src.agents.validator_equipment import ValidatorEquipment
from src.agents.specific_search import run_specific_research
from src.agents.extract_specific_results import extract_specific_infos
from utils.tavily_search_provider import TavilySearch
from utils.llm_service import LLMService

app = Flask(__name__)

# Created once when the server starts — same dependency-injection
# pattern as main.py, so caching etc. still works across requests.
llm_service = LLMService()
tavily = TavilySearch()
resolver = EquipementResolver(llm_service)
router = RouterEntityType()
validator = ValidatorEquipment(tavily, llm_service)

PAGE = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Pipeline Debug</title>
<style>
  body { font-family: monospace; background: #1e1e1e; color: #ddd; padding: 30px; }
  input[type=text] { width: 400px; padding: 8px; font-size: 16px; }
  button { padding: 8px 16px; font-size: 16px; margin-left: 10px; }
  pre { background: #2a2a2a; padding: 15px; border-radius: 6px; white-space: pre-wrap; word-wrap: break-word; }
</style>
</head>
<body>
  <h2>Equipment Pipeline Debug</h2>
  <form method="post">
    <input type="text" name="equipment_name" placeholder="ex: Grundfos CR 15-4" value="{{ equipment_name or '' }}">
    <input type="text" name="hint" placeholder="hint (optionnel)" value="{{ hint or '' }}">
    <button type="submit">Run</button>
  </form>

  {% if error %}
    <h3 style="color: #ff6b6b;">Erreur</h3>
    <pre>{{ error }}</pre>
  {% endif %}

  {% if result %}
    <h3>Résultat</h3>
    <pre>{{ result }}</pre>
  {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    equipment_name = None
    hint = None
    result = None
    error = None

    if request.method == "POST":
        equipment_name = request.form.get("equipment_name", "").strip()
        hint = request.form.get("hint", "").strip()

        try:
            entity = resolver.resolve(equipment_name)
            decision = router.route(entity)

            if decision == "SPECIFIC":
                sources = run_specific_research(entity, sources=[], tavily_search=tavily, llm=llm_service)
                final = extract_specific_infos(entity, sources, tavily, llm_service, hint)
            elif decision == "UNCERTAIN":
                val = validator.validate(entity)
                final = {"decision": "UNCERTAIN", "validator_result": val}
            else:
                final = {"decision": "GENERAL", "note": "Pas encore implémenté"}

            result = json.dumps(
                {"entity": entity.model_dump(), "decision": decision, "final": final},
                indent=2,
                ensure_ascii=False,
            )
        except Exception as e:
            error = f"{type(e).__name__}: {e}"

    return render_template_string(PAGE, equipment_name=equipment_name, hint=hint, result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True, port=5000)