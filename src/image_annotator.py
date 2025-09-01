import json
import csv
from pathlib import Path
from PIL import Image
from transformers import ViTFeatureExtractor, ViTForImageClassification
import torch

# Load pre-trained model
feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224")
model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")

def read_images(input_dir):
    """Read supported images from a directory."""
    input_path = Path(input_dir)
    if not input_path.is_dir():
        raise ValueError(f"{input_dir} is not a directory")
    
    supported_exts = {".png", ".jpg", ".jpeg"}
    data = []

    for img_file in input_path.iterdir():
        if img_file.suffix.lower() in supported_exts:
            data.append({"image": str(img_file), "name": img_file.name})
    
    return data

def classify_image(img_path):
    """Classify a single image with the ViT model."""
    try:
        image = Image.open(str(img_path)).convert("RGB")
        image = image.resize((224, 224))  # enforce ViT expected size
    except Exception as e:
        print(f"⚠️ Skipping {img_path} (cannot open: {e})")
        return "unreadable"

    inputs = feature_extractor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    label = model.config.id2label[predicted_class_idx]
    return label

def annotate_images(input_dir, output_path):
    """Annotate all images in a directory and save results."""
    data = read_images(input_dir)

    for entry in data:
        label = classify_image(entry["image"])
        entry["labels"] = [label]
        print(f"🔍 {entry['name']} → {label}")

    ext = Path(output_path).suffix.lower()
    if ext == ".json":
        serializable_data = [
            {"image": entry["name"], "labels": entry["labels"]}
            for entry in data
        ]
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(serializable_data, f, indent=2)

    elif ext == ".csv":
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["image", "labels"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow({"image": entry["name"], "labels": ";".join(entry["labels"])})
    else:
        raise ValueError(f"Unsupported output format: {ext}")

    return data

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Annotate images with Hugging Face ViT model")
    parser.add_argument("input_dir", help="Directory containing images")
    parser.add_argument("output_path", help="Output JSON/CSV file")
    args = parser.parse_args()

    results = annotate_images(args.input_dir, args.output_path)
    print(f"✅ Annotated {len(results)} images → {args.output_path}")
