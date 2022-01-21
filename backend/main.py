from fastapi import FastAPI
from security import auth
from util import find, save, get_authorized_thoughts, remove
from sentence_transformers import SentenceTransformer
from fastapi.datastructures import UploadFile
from fastapi import FastAPI, File, Form
from fastapi.responses import FileResponse
from pathlib import Path
from microverses import create_microverse, remove_microverse, list_microverses


app = FastAPI()
text_image_encoder = SentenceTransformer('clip-ViT-B-32')
text_encoder = SentenceTransformer(
    'sentence-transformers/multi-qa-mpnet-base-cos-v1')


@app.get('/find')
async def find_text_handler(query: str, token: str):
    auth_result = auth(token)
    results = find('text', query, auth_result,
                   text_encoder, text_image_encoder)
    return results


@app.post('/find')
async def find_image_handler(query: UploadFile = File(...), token: str = Form(...)):
    query = await query.read()
    auth_result = auth(token)
    results = find('image', query, auth_result,
                   text_encoder, text_image_encoder)
    return results


@app.get('/save')
async def save_text_handler(query: str, token: str):
    auth_result = auth(token)
    results = save('text', query, auth_result,
                   text_encoder, text_image_encoder)
    return results


@app.post('/save')
async def save_image_handler(query: UploadFile = File(...), token: str = Form(...)):
    query = await query.read()
    auth_result = auth(token)
    results = save('image', query, auth_result,
                   text_encoder, text_image_encoder)
    return results


@app.get('/remove')
async def remove_handler(filename: str, token: str):
    auth_result = auth(token)
    return remove(auth_result, filename)


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
    return create_microverse('text', query, auth_result, text_encoder, text_image_encoder)


@app.post('/microverse/create')
async def microverse_create_handler(query: UploadFile = File(...), token: str = Form(...)):
    query = await query.read()
    auth_result = auth(token)
    return create_microverse('image', query, auth_result, text_encoder, text_image_encoder)


@app.get('/microverse/remove')
async def microverse_remove_handler(token: str, microverse: str):
    auth_result = auth(token)
    return remove_microverse(auth_result, microverse)


@app.get('/microverse/list')
async def microverse_list_handler(token: str):
    auth_result = auth(token)
    return list_microverses(auth_result)


@app.get('/custodian/check')
async def check_custodian(token: str):
    return auth(token)
