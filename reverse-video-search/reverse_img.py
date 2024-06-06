from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

def load_image(image_path):
    return Image.open(image_path)

def get_image_embeddings(image_paths, model, processor):
    images = [load_image(img_path) for img_path in image_paths]
    inputs = processor(images=images, return_tensors="pt", padding=True)
    outputs = model.get_image_features(**inputs)
    return outputs

def cosine_similarity(embeddings1, embeddings2):
    normalized_embeddings1 = embeddings1 / embeddings1.norm(dim=1, keepdim=True)
    normalized_embeddings2 = embeddings2 / embeddings2.norm(dim=1, keepdim=True)
    return torch.mm(normalized_embeddings1, normalized_embeddings2.transpose(0, 1))

# Initialize CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Embed three images
image_paths = ["path/to/image1.jpg", "path/to/image2.jpg", "path/to/image3.jpg"]
embeddings = get_image_embeddings(image_paths, model, processor)

# Accept a new image for reverse image search
new_image_path = "path/to/new_image.jpg"
new_image_embedding = get_image_embeddings([new_image_path], model, processor)

# Compute similarities
similarities = cosine_similarity(new_image_embedding, embeddings)
most_similar_index = similarities.argmax()

print(f"The most similar image is at index: {most_similar_index.item()} and path: {image_paths[most_similar_index.item()]}")