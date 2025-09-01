from PIL import Image
from pathlib import Path

img_dir = Path("data/images")
for img in img_dir.iterdir():
    try:
        im = Image.open(img)
        im.verify()  # just verifies integrity, doesn't load
        print(f"✅ {img.name} is fine")
    except Exception as e:
        print(f"❌ {img.name} is broken: {e}")
