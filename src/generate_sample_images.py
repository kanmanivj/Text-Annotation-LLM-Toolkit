from PIL import Image, ImageDraw, ImageFont
import os

def generate_sample_images(output_dir="data/images", num_images=5):
    os.makedirs(output_dir, exist_ok=True)

    for i in range(num_images):
        # Create a blank image (RGB)
        img = Image.new("RGB", (200, 200), color=(i * 40 % 255, i * 80 % 255, i * 120 % 255))
        
        # Draw text
        draw = ImageDraw.Draw(img)
        text = f"Img {i+1}"
        try:
            font = ImageFont.load_default()
        except:
            font = None
        draw.text((50, 90), text, fill=(255, 255, 255), font=font)

        # Save
        img_path = os.path.join(output_dir, f"sample_{i+1}.png")
        img.save(img_path)
        print(f"Generated {img_path}")

if __name__ == "__main__":
    generate_sample_images()
