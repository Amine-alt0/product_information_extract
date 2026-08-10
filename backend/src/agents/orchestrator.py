import os 
import logging
from agents.equipment_resolver import Equipemenentity
from agents.router_entity_status import RouterEntityType
from validator_equipment import ValidatorEquipment

logger=logging.getLogger(__name__)


class RouterSearchPlan:
    def __init__(self):
        pass
    def process_equipment(name: str, resolver, router, validator):
        entity = resolver.resolve(name)
        decision = router.route(entity)

        if decision == "SPECIFIC":
            return run_specific_research(entity, sources=[])

        if decision == "UNCERTAIN":
            result = validator.validate(entity)

            if result["status"] == "VALID":
                entity.manufacturer = result["manufacturer"] or entity.manufacturer
                entity.model = result["model"] or entity.model
                return run_specific_research(entity, sources=result["sources"])
            else:
                return run_general_research(entity, sources=result["sources"])

        # decision == "GENERAL"
        return run_general_research(entity, sources=[])
            