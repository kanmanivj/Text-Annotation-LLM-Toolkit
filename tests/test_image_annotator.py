from src.image_annotator import annotate_images

annotations = annotate_images("data/images", "data/image_output.json", labels=["cat", "animal"])
print(annotations)
