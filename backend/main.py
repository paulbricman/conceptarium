from fastapi import FastAPI, Request, Header
from security import auth
from util import find, rank, save, get_authorized_thoughts, remove, dump
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
    relatedness: float = 0.8,
    activation: float = 0.,
    noise: float = 0.1,
    return_embeddings: bool = False,
    silent: bool = False,
    request: Request = None,
    authorization: str = Header(None)
):
    return find(
        'text',
        query,
        relatedness,
        activation,
        noise,
        return_embeddings,
        auth(authorization),
        text_encoder,
        text_image_encoder,
        silent
    )


@app.post('/find', response_class=ORJSONResponse)
async def find_image_handler(
    query: UploadFile = File(...),
    relatedness: float = Form(0.8),
    activation: float = Form(0.),
    noise: float = Form(0.1),
    return_embeddings: bool = Form(False),
    silent: bool = Form(False),
    request: Request = None,
    authorization: str = Header(None)
):
    query = await query.read()
    return find(
        'image',
        query,
        relatedness,
        activation,
        noise,
        return_embeddings,
        auth(authorization),
        text_encoder,
        text_image_encoder,
        silent
    )


@app.get('/save')
async def save_text_handler(query: str, request: Request, authorization: str = Header(None)):
    return save('text', query, auth(authorization),
                text_encoder, text_image_encoder)


@app.post('/save')
async def save_image_handler(query: UploadFile = File(...), request: Request = None, authorization: str = Header(None)):
    query = await query.read()
    results = save('image', query, auth(authorization),
                   text_encoder, text_image_encoder)
    return results


@app.get('/remove')
async def remove_handler(filename: str, request: Request, authorization: str = Header(None)):
    return remove(auth(authorization), filename)


@app.get('/dump')
async def save_text_handler(request: Request, authorization: str = Header(None)):
    return dump(auth(authorization))


@app.get('/static')
@limiter.limit("200/minute")
async def static_handler(filename: str, request: Request, authorization: str = Header(None)):
    knowledge_base_path = Path('..') / 'knowledge'
    thoughts = get_authorized_thoughts(auth(authorization))
    if filename in [e['filename'] for e in thoughts]:
        return FileResponse(knowledge_base_path / filename)


@app.get('/microverse/create')
async def microverse_create_handler(query: str, request: Request, authorization: str = Header(None)):
    return create_microverse('text', query, auth(authorization), text_encoder, text_image_encoder)


@app.post('/microverse/create')
async def microverse_create_handler(query: UploadFile = File(...), request: Request = None, authorization: str = Header(None)):
    query = await query.read()
    return create_microverse('image', query, auth(authorization), text_encoder, text_image_encoder)


@app.get('/microverse/remove')
async def microverse_remove_handler(microverse: str, request: Request, authorization: str = Header(None)):
    return remove_microverse(auth(authorization), microverse)


@app.get('/microverse/list')
async def microverse_list_handler(request: Request, authorization: str = Header(None)):
    return list_microverses(auth(authorization))


@app.get('/custodian/check')
async def check_custodian(request: Request, authorization: str = Header(None)):
    return auth(authorization)
