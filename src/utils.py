# src/utils.py
import re

def clean_text(text):
    """
    Simple text cleaning: lowercasing and trimming whitespace.
    """
    return text.lower().strip()

def extract_emails(text):
    """
    Regex to extract emails from a text string.
    """
    return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", text)
