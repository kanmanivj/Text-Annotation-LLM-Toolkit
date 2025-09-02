import json
import csv
from pathlib import Path
from PIL import Image
from transformers import ViTFeatureExtractor, ViTForImageClassification
import torch
import asyncio

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

# def classify_image(img_path):
#     """Classify a single image with the ViT model."""
#     try:
#         image = Image.open(str(img_path)).convert("RGB")
#         image = image.resize((224, 224))  # enforce ViT expected size
#     except Exception as e:
#         print(f"⚠️ Skipping {img_path} (cannot open: {e})")
#         return "unreadable"

#     inputs = feature_extractor(images=image, return_tensors="pt")
#     outputs = model(**inputs)
#     logits = outputs.logits
#     predicted_class_idx = logits.argmax(-1).item()
#     label = model.config.id2label[predicted_class_idx]
#     return label

def save_results(data, output_path):
    """Save annotated results to JSON or CSV."""
    ext = Path(output_path).suffix.lower()

    if ext == ".json":
        serializable_data = [
            {"image": Path(entry["image"]).name, "labels": entry["labels"]}
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
                writer.writerow({
                    "image": Path(entry["image"]).name,
                    "labels": ";".join(entry["labels"])
                })
    else:
        raise ValueError(f"Unsupported output format: {ext}")


def classify_images_batch(image_paths, batch_size=8):
    """Classify a batch of images with the ViT model."""
    images = []
    valid_paths = []

    for img_path in image_paths:
        try:
            img = Image.open(str(img_path)).convert("RGB")
            img = img.resize((224, 224))
            images.append(img)
            valid_paths.append(img_path)
        except Exception as e:
            print(f"⚠️ Skipping {img_path} (cannot open: {e})")

    if not images:
        return {}

    inputs = feature_extractor(images=images, return_tensors="pt")

    # ✅ GPU Support
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        preds = outputs.logits.argmax(-1).cpu().numpy()

    labels = [model.config.id2label[idx] for idx in preds]
    return dict(zip(valid_paths, labels))

async def process_image_batches(image_files, batch_size=8):
    results = {}
    for i in range(0, len(image_files), batch_size):
        batch = image_files[i:i+batch_size]
        batch_results = classify_images_batch(batch, batch_size=batch_size)
        results.update(batch_results)
        await asyncio.sleep(0)  # yield control (cooperative multitasking)
    return results

def annotate_images(input_dir, output_path, batch_size=8, limit=None):
    """Annotate images in a directory and save results."""
    
    data = read_images(input_dir)

    if limit:
        data = data[:limit]  # only keep first N entries

    image_files = [Path(entry["image"]) for entry in data]

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(process_image_batches(image_files, batch_size))

    for entry in data:
        label = results.get(Path(entry["image"]), "unreadable")
        entry["labels"] = [label]
        print(f"🔍 {entry['name']} → {label}")

    save_results(data, output_path)
    return data



if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Annotate images with Hugging Face ViT model")
    parser.add_argument("input_dir", help="Directory containing images")
    parser.add_argument("output_path", help="Output JSON/CSV file")
    args = parser.parse_args()

    results = annotate_images(args.input_dir, args.output_path)

    print(f"✅ Annotated {len(results)} images → {args.output_path}")
    
