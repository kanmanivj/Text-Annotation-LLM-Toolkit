# src/annotator.py
import json
from src.utils import clean_text

def annotate_text(text, label):
    """
    Annotates a single text with a label.
    Returns a dictionary.
    """
    cleaned_text = clean_text(text)
    return {"text": cleaned_text, "label": label}

def annotate_file(input_file, output_file, label="general"):
    """
    Reads JSON input file, annotates each text, writes output JSON.
    """
    with open(input_file, "r") as f:
        data = json.load(f)

    annotations = [annotate_text(item, label) for item in data]

    with open(output_file, "w") as f:
        json.dump(annotations, f, indent=2)
    return annotations
