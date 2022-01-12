from fastapi import FastAPI
from security import auth
from util import find, save, get_authorized_thoughts
from sentence_transformers import SentenceTransformer
from fastapi.datastructures import UploadFile
from fastapi import FastAPI, File, Form
from fastapi.responses import FileResponse
from pathlib import Path
from microverses import create_microverse, remove_microverse


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


@app.get('/static')
async def static_handler(filename: str, token: str):
    knowledge_base_path = Path('..') / 'knowledge' / 'base'

    auth_result = auth(token)
    thoughts = get_authorized_thoughts(auth_result)
    if filename in [e['filename'] for e in thoughts]:
        return FileResponse(knowledge_base_path / filename)


@app.get('/microverse/create')
async def microverse_create_handler(query: str, token: str):
    auth_result = auth(token)
    return create_microverse('text', query, auth_result, encoder_model)


@app.post('/microverse/create')
async def microverse_create_handler(query: UploadFile = File(...), token: str = Form(...)):
    query = await query.read()
    auth_result = auth(token)
    return create_microverse('image', query, auth_result, encoder_model)


@app.get('/microverse/remove')
async def microverse_remove_handler(custodian_token: str, microverse_token):
    auth_result = auth(custodian_token)
    return remove_microverse(auth_result, microverse_token)
