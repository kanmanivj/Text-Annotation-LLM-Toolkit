from src.annotator import annotate_file

# Test JSON annotation
annotations_json = annotate_file("data/input.json", "data/output.json", labels=["general", "technical"])
print("JSON Annotations:", annotations_json)

# Test CSV annotation
annotations_csv = annotate_file("data/input.csv", "data/output.csv", labels=["general", "business"])
print("CSV Annotations:", annotations_csv)

# Test Markdown annotation
annotations_md = annotate_file("data/input.md", "data/output.md", labels=["general", "technical"])
print("Markdown Annotations:", annotations_md)
