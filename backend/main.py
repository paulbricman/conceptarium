from fastapi import FastAPI
from security import auth
from util import find
from sentence_transformers import SentenceTransformer


app = FastAPI()
encoder_model = SentenceTransformer('clip-ViT-B-32')


@app.get('/find')
async def find_handler(query: str, token: str):
    auth_result = auth(token)
    results = find('text', query, auth_result, encoder_model)
    return results
