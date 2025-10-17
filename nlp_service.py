import spacy
import re
from config import settings

# Load the spaCy model. It's good practice to load this once when the module is imported.
# This model needs to be downloaded separately.
nlp = spacy.load(settings.SPACY_MODEL)

# Regex patterns for different IOC types
IOC_PATTERNS = {
    "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "md5": r"\b[a-fA-F0-9]{32}\b",
    "sha256": r"\b[a-fA-F0-9]{64}\b",
    "domain": r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}\b",
    "cve": r"\bCVE-\d{4}-\d{4,7}\b",
}


def extract_intelligence(text: str) -> dict:
    """
    Extracts named entities from text using spaCy and IOCs using regex.
    """
    # Process the text with the spaCy pipeline
    doc = nlp(text)

    # Extract entities and format them
    entities = []
    for ent in doc.ents:
        entities.append({"text": ent.text, "label": ent.label_})

    # Extract IOCs using regular expressions
    iocs = []
    for ioc_type, pattern in IOC_PATTERNS.items():
        for match in re.finditer(pattern, text):
            # Avoid adding duplicates that spaCy might also find (like some CVEs)
            if match.group(0) not in [e["text"] for e in entities]:
                iocs.append({"value": match.group(0), "type": ioc_type})

    return {"entities": entities, "iocs": iocs}