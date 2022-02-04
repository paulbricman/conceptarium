from fastapi import FastAPI, Request
from security import auth
from util import find, rank, save, get_authorized_thoughts, remove
from sentence_transformers import SentenceTransformer
from fastapi.datastructures import UploadFile
from fastapi import FastAPI, File, Form
from fastapi.responses import FileResponse, ORJSONResponse
from pathlib import Path
from microverses import create_microverse, remove_microverse, list_microverses
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded


limiter = Limiter(key_func=get_remote_address, default_limits=['30/minute'])
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

text_image_encoder = SentenceTransformer('clip-ViT-B-32')
text_encoder = SentenceTransformer(
    'sentence-transformers/multi-qa-mpnet-base-cos-v1')


@app.get('/find', response_class=ORJSONResponse)
async def find_text_handler(
    query: str,
    token: str,
    relatedness: float = 0.8,
    activation: float = 0.,
    noise: float = 0.1,
    return_embeddings: bool = False,
    silent: bool = False,
    request: Request = None
):
    return find(
        'text',
        query,
        relatedness,
        activation,
        noise,
        return_embeddings,
        auth(token),
        text_encoder,
        text_image_encoder,
        silent
    )


@app.post('/find', response_class=ORJSONResponse)
async def find_image_handler(
    query: UploadFile = File(...),
    token: str = Form(...),
    relatedness: float = Form(0.8),
    activation: float = Form(0.),
    noise: float = Form(0.1),
    return_embeddings: bool = Form(False),
    silent: bool = Form(False),
    request: Request = None
):
    query = await query.read()
    return find(
        'image',
        query,
        relatedness,
        activation,
        noise,
        return_embeddings,
        auth(token),
        text_encoder,
        text_image_encoder,
        silent
    )


@app.get('/save')
async def save_text_handler(query: str, token: str, request: Request):
    auth_result = auth(token)
    results = save('text', query, auth_result,
                   text_encoder, text_image_encoder)
    return results


@app.post('/save')
async def save_image_handler(query: UploadFile = File(...), token: str = Form(...), request: Request = None):
    query = await query.read()
    auth_result = auth(token)
    results = save('image', query, auth_result,
                   text_encoder, text_image_encoder)
    return results


@app.get('/remove')
async def remove_handler(filename: str, token: str, request: Request):
    auth_result = auth(token)
    return remove(auth_result, filename)


@app.get('/static')
@limiter.limit("200/minute")
async def static_handler(filename: str, token: str, request: Request):
    knowledge_base_path = Path('..') / 'knowledge'

    auth_result = auth(token)
    thoughts = get_authorized_thoughts(auth_result)
    if filename in [e['filename'] for e in thoughts]:
        return FileResponse(knowledge_base_path / filename)


@app.get('/microverse/create')
async def microverse_create_handler(query: str, token: str, request: Request):
    auth_result = auth(token)
    return create_microverse('text', query, auth_result, text_encoder, text_image_encoder)


@app.post('/microverse/create')
async def microverse_create_handler(query: UploadFile = File(...), token: str = Form(...), request: Request = None):
    query = await query.read()
    auth_result = auth(token)
    return create_microverse('image', query, auth_result, text_encoder, text_image_encoder)


@app.get('/microverse/remove')
async def microverse_remove_handler(token: str, microverse: str, request: Request):
    auth_result = auth(token)
    return remove_microverse(auth_result, microverse)


@app.get('/microverse/list')
async def microverse_list_handler(token: str, request: Request):
    auth_result = auth(token)
    return list_microverses(auth_result)


@app.get('/custodian/check')
async def check_custodian(token: str, request: Request):
    return auth(token)
