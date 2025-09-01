import json
import csv
from pathlib import Path

def classify_image(img_path):
    try:
        image = Image.open(img_path).convert("RGB")
    except Exception as e:
        print(f"⚠️ Skipping {img_path} (cannot open: {e})")
        return "unreadable"

    inputs = feature_extractor(images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    label = model.config.id2label[predicted_class_idx]
    return label


def read_input(file_path):
    ext = Path(file_path).suffix.lower()
    data = []
    
    if ext == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure each entry is a dict with 'text'
            data = [{"text": x["text"]} if isinstance(x, dict) else {"text": x} for x in data]
    
    elif ext == ".csv":
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            data = [{"text": row["text"]} for row in reader]
    
    elif ext in [".md", ".txt"]:
        with open(file_path, "r", encoding="utf-8") as f:
            data = [{"text": line.strip()} for line in f if line.strip()]
    
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    
    return data

def write_output(data, file_path):
    ext = Path(file_path).suffix.lower()
    
    if ext == ".json":
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    
    elif ext == ".csv":
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["text", "labels"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow({
                    "text": entry["text"],
                    "labels": ";".join(entry["labels"])
                })
    
    elif ext in [".md", ".txt"]:
        with open(file_path, "w", encoding="utf-8") as f:
            for entry in data:
                labels_str = ", ".join(entry["labels"])
                f.write(f"{entry['text']} | Labels: {labels_str}\n")
    
    else:
        raise ValueError(f"Unsupported output format: {ext}")


def annotate_file(input_path, output_path, labels=None):
    """
    Annotate a file with multi-label support.
    labels: list of strings
    """
    if labels is None:
        labels = ["general"]  # default label

    data = read_input(input_path)
    
    for entry in data:
        entry["labels"] = labels  # Assign multiple labels
    
    write_output(data, output_path)
    return data
