from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from nlp_service import extract_intelligence
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class TextInput(BaseModel):
    text: str

# --- Output Models ---
class Entity(BaseModel):
    text: str
    label: str

class IOC(BaseModel):
    value: str
    type: str

class AnalysisResponse(BaseModel):
    entities: List[Entity]
    iocs: List[IOC]


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(data: TextInput):
    try:
        logger.info(f"Analyzing text of length {len(data.text)}...")
        # Call the NLP service with the input text
        intelligence = extract_intelligence(data.text)
        logger.info(f"Analysis complete. Found {len(intelligence['entities'])} entities and {len(intelligence['iocs'])} IOCs.")
        return intelligence
    except Exception as e:
        logger.error(f"An error occurred during text analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal error occurred during analysis.")