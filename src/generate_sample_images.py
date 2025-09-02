from datasets import load_dataset

# Load CIFAR-10 (tiny images, 60k total, 10 classes)
dataset = load_dataset("cifar10")

# Save 50 sample images into data/images/
import os
from PIL import Image

os.makedirs("data/images", exist_ok=True)

for i in range(50):
    img = dataset["train"][i]["img"]  # PIL image
    img.save(f"data/images/sample_{i}.jpg")
