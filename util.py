from sentence_transformers import SentenceTransformer
from PIL import Image
import io


def load_model():
    return SentenceTransformer('clip-ViT-B-32')


def embed(content, model):
    if isinstance(content, str):
        return model.encode([content])
    else:
        return model.encode(Image.open(io.BytesIO(content)))
