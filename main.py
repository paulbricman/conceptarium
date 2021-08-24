from fastapi import FastAPI, File
from fastapi.datastructures import UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse
import secrets
from pathlib import Path
from typing import Optional

from util import *
from responses import *

app = FastAPI()
model = load_model()
init()

app.mount('/conceptarium', StaticFiles(directory='conceptarium'))


@app.get('/save/lang')
async def save_language(content: str):
    if len(content) > 3:
        filename = 'conceptarium/' + secrets.token_urlsafe(8) + '.txt'
        open(filename, 'w').write(content)
        save(Thought(filename, content, model))


@app.post('/save/imag')
async def save_imagery(file: UploadFile = File(...)):
    content = await file.read()
    extension = Path(file.filename).suffix
    filename = 'conceptarium/' + \
        secrets.token_urlsafe(8) + extension
    open(filename, 'wb+').write(content)
    save(Thought(filename, content, model))


@app.get('/find/lang/html')
async def find_by_language_return_html(content: str, relatedness: Optional[float] = 1, activation: Optional[float] = 0, noise: Optional[float] = 0.05, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    thoughts = find(content, model, relatedness,
                    activation, noise, silent, top_k)
    return HTMLResponse(html_response(thoughts))


@app.get('/find/lang/text')
async def find_by_language_return_plaintext(content: str, relatedness: Optional[float] = 1, activation: Optional[float] = 0, noise: Optional[float] = 0.05, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    thoughts = find(content, model, relatedness,
                    activation, noise, silent, top_k)
    return PlainTextResponse(plaintext_response(thoughts))


@app.get('/find/lang/file')
async def find_by_language_return_file(content: str, relatedness: Optional[float] = 1, activation: Optional[float] = 0, noise: Optional[float] = 0.05, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    thoughts = find(content, model, relatedness,
                    activation, noise, silent, top_k)
    return FileResponse(file_response(thoughts))


@app.get('/find/lang/json')
async def find_by_language_return_json(content: str, relatedness: Optional[float] = 1, activation: Optional[float] = 0, noise: Optional[float] = 0.05, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    thoughts = find(content, model, relatedness,
                    activation, noise, silent, top_k)
    return json_response(thoughts)


@app.post('/find/imag/html')
async def find_by_imagery_return_html(file: UploadFile = File(...), relatedness: Optional[float] = 1, activation: Optional[float] = 0, noise: Optional[float] = 0.05, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    content = await file.read()
    thoughts = find(content, model, relatedness,
                    activation, noise, silent, top_k)
    return HTMLResponse(html_response(thoughts))


@app.post('/find/imag/text')
async def find_by_imagery_return_plaintext(file: UploadFile = File(...), relatedness: Optional[float] = 1, activation: Optional[float] = 0, noise: Optional[float] = 0.05, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    content = await file.read()
    thoughts = find(content, model, relatedness,
                    activation, noise, silent, top_k)
    return PlainTextResponse(plaintext_response(thoughts))


@app.post('/find/imag/file')
async def find_by_imagery_return_file(file: UploadFile = File(...), relatedness: Optional[float] = 1, activation: Optional[float] = 0, noise: Optional[float] = 0.05, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    content = await file.read()
    thoughts = find(content, model, relatedness,
                    activation, noise, silent, top_k)
    return FileResponse(file_response(thoughts))


@app.post('/find/imag/json')
async def find_by_imagery_return_json(file: UploadFile = File(...), relatedness: Optional[float] = 1, activation: Optional[float] = 0, noise: Optional[float] = 0.05, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    content = await file.read()
    thoughts = find(content, model, relatedness,
                    activation, noise, silent, top_k)
    return json_response(thoughts)


@app.get('/rset/embs')
async def reset_embeddings_handle():
    reset_embeddings(model)
