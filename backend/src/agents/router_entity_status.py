import os 
from src.agents.validator_equipment import Equipemenentity
import logging
import json
from datetime import datetime, timezone

logger=logging.getLogger(__name__)

class RouterEntityType:
    def __init__(self,log_path="router_decisions.jsonl"):
        self.log_path = log_path
        pass
    def route(self, entity: Equipemenentity) -> str:
        decision = self.planner(entity)
        self._log(entity, decision)
        return decision

    def planner(self,entity:Equipemenentity):
        
        if (
        entity.manufacturer
        and entity.model
        and entity.confidence >= 0.7
        and not entity.ambiguity
    ):
            return "SPECIFIC"

        if (
            entity.model
            or entity.manufacturer
            or entity.ambiguity
        ):
            return "UNCERTAIN"

        return "GENERAL"
    def _log(self, entity: Equipemenentity, decision: str):
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input": entity.model_dump(),
            "decision": decision,
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")