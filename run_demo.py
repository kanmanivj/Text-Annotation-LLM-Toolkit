# run_demo.py
from src.annotator import annotate_file

annotations = annotate_file("data/input.json", "data/output.json", label="general")
print(annotations)
