import json
import csv
from pathlib import Path

def read_images(input_dir):
    """
    Read all images from a directory.
    Returns a list of dicts: [{"image": "filename.png"}]
    """
    input_path = Path(input_dir)
    if not input_path.is_dir():
        raise ValueError(f"{input_dir} is not a directory")

    supported_exts = {".png", ".jpg", ".jpeg"}
    data = []

    for img_file in input_path.iterdir():
        if img_file.suffix.lower() in supported_exts:
            data.append({"image": img_file.name})

    return data


def write_output(data, file_path):
    """
    Write annotations to JSON or CSV.
    """
    ext = Path(file_path).suffix.lower()

    if ext == ".json":
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    elif ext == ".csv":
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["image", "labels"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow({"image": entry["image"], "labels": ";".join(entry["labels"])})

    else:
        raise ValueError(f"Unsupported output format: {ext}")


def annotate_images(input_dir, output_path, labels=None):
    """
    Annotate all images in a directory with multi-label support.
    labels: list of strings
    """
    if labels is None:
        labels = ["unlabeled"]

    data = read_images(input_dir)

    for entry in data:
        entry["labels"] = labels  # assign same labels for now

    write_output(data, output_path)
    return data


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Annotate images with labels")
    parser.add_argument("input_dir", help="Directory containing images")
    parser.add_argument("output_path", help="Output JSON/CSV file")
    parser.add_argument("--labels", nargs="+", default=["unlabeled"], help="Labels to assign")

    args = parser.parse_args()

    results = annotate_images(args.input_dir, args.output_path, args.labels)
    print(f"Annotated {len(results)} images → {args.output_path}")
