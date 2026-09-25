from flask import Flask, request, render_template_string, jsonify
import json
import threading
from src.agents.equipment_resolver import EquipementResolver
from src.agents.router_entity_status import RouterEntityType
from src.agents.validator_equipment import ValidatorEquipment
from src.agents.specific_search import run_specific_research
from src.agents.extract_specific_results import extract_specific_infos
from utils.tavily_search_provider import TavilySearch
from utils.llm_service import LLMService
from utils.utility_funcs import PipelineCache
from src.agents.orchestrator import process_equipment

import logging
cancel_flags={}
cancel_flags_lock = threading.Lock()

app = Flask(__name__)
logger = logging.getLogger(__name__)
# Created once when the server starts — same dependency-injection
# pattern as main.py, so caching etc. still works across requests.
llm_service = LLMService()
tavily = TavilySearch()
cache = PipelineCache()
resolver = EquipementResolver(llm_service)
router = RouterEntityType()
validator = ValidatorEquipment(tavily, llm_service)
def set_cancel_flags(request_id:str):
    with cancel_flags_lock:
        cancel_flags[request_id] = True
    return True

def _run_pipeline(equipment_name: str, hint: str,request_id:str):
    with cancel_flags_lock:
        cancel_flags[request_id] = False
        
    try :
        return process_equipment(
        equipment_name,
        resolver,
        router,
        validator,
        tavily,
        llm_service,
        hint,
        cache,
    )
    finally:
        with cancel_flags_lock:
            cancel_flags.pop(request_id,None)
    

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

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
            final = _run_pipeline(equipment_name, hint)

            result = json.dumps(
                final,
                indent=2,
                ensure_ascii=False,
                default=str
            )

        except Exception as e:
            error = f"{type(e).__name__}: {e}"

    return render_template_string(
        PAGE,
        equipment_name=equipment_name,
        hint=hint,
        result=result,
        error=error
    )


@app.route("/api/search", methods=["POST", "OPTIONS"])
def api_search():
    if request.method == "OPTIONS":
        return ("", 204)

    payload = request.get_json(silent=True) or {}
    equipment_name = (payload.get("equipment_name") or "").strip()
    hint = (payload.get("hint") or "").strip()
    request_id=(payload.get("request_id") or "").strip()
    if not equipment_name:
        return jsonify({"error": "equipment_name is required"}), 400

    try:
        final = _run_pipeline(equipment_name, hint,request_id)
        return jsonify(final)
    except Exception as e:
        logger.exception("Pipeline error during /api/search")
        return jsonify({"error": f"{type(e).__name__}: {e}"}), 500

@app.route("/api/cancel/<request_id>",methods=["POST", "OPTIONS"])
def api_cancel(request_id):
    if request.method == "OPTIONS":
        return ("", 204)
    try:
        answer=set_cancel_flags(request_id)
        return jsonify({"status": "cancel requested"})
    except Exception as e:
        logger.exception("cancelation error during /api/search")
        return jsonify({"error": f"{type(e).__name__}: {e}"}), 500
if __name__ == "__main__":
  app.run(debug=True, use_reloader=False, port=5001,threaded=True)