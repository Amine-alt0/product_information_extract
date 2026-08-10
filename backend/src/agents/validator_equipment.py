import os 
import logging
from pydantic import BaseModel
from logger import setup_logger
from utils.llm_service import LLMService
import json
from agents.equipment_resolver import Equipemenentity


setup_logger()

logger=logging.getLogger(__name__)



class ValidationResult(BaseModel):
    status: str
    manufacturer_verified: bool
    model_verified: bool
    source_type: str | None
    source_url: str | None
    confidence: float

class ValidatorEquipment:
    def __init__(self):
        pass
    
    def validate(self,EquipemntEntity):
        logger.info(
            " cheking the results... "
        )
        