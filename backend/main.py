from fastapi import FastAPI
from security import auth
from util import find, save
from sentence_transformers import SentenceTransformer
from fastapi.datastructures import UploadFile
from fastapi import FastAPI, File, Form


app = FastAPI()
encoder_model = SentenceTransformer('clip-ViT-B-32')


@app.get('/find')
async def find_text_handler(query: str, token: str):
    auth_result = auth(token)
    results = find('text', query, auth_result, encoder_model)
    return results


@app.post('/find')
async def find_image_handler(query: UploadFile = File(...), token: str = Form(...)):
    query = await query.read()
    auth_result = auth(token)
    results = find('image', query, auth_result, encoder_model)
    return results


@app.get('/save')
async def save_text_handler(query: str, token: str):
    auth_result = auth(token)
    results = save('text', query, auth_result, encoder_model)
    return results


@app.post('/save')
async def save_image_handler(query: UploadFile = File(...), token: str = Form(...)):
    query = await query.read()
    auth_result = auth(token)
    results = save('image', query, auth_result, encoder_model)
    return results
