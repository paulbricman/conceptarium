from fastapi import FastAPI, File, BackgroundTasks
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
app.mount('/assets', StaticFiles(directory='assets'))


@app.get('/save/lang')
async def save_language(content: str, background_tasks: BackgroundTasks):
    if len(content) > 3:
        filename = 'conceptarium/' + secrets.token_urlsafe(8) + '.txt'
        open(filename, 'w').write(content)
        background_tasks.add_task(save, Thought(filename, content, model))
        return HTMLResponse(success_response())


@app.post('/save/imag')
async def save_imagery(file: UploadFile = File(...)):
    content = await file.read()
    extension = Path(file.filename).suffix
    filename = 'conceptarium/' + \
        secrets.token_urlsafe(8) + extension
    open(filename, 'wb+').write(content)
    save(Thought(filename, content, model))
    return HTMLResponse(success_response())


@app.get('/save/lang/form')
async def save_language_form():
    return HTMLResponse(lang_form_response())


@app.get('/save/imag/form')
async def save_imagery_form():
    return HTMLResponse(imag_form_response())


@app.get('/find/lang/html')
async def find_by_language_return_html(content: str, relatedness: Optional[float] = 1, serendipity: Optional[float] = 0, noise: Optional[float] = 0.01, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    thoughts = find(content, model, relatedness,
                    serendipity, noise, silent, top_k)
    return HTMLResponse(html_response(thoughts))


@app.get('/find/lang/text')
async def find_by_language_return_plaintext(content: str, relatedness: Optional[float] = 1, serendipity: Optional[float] = 0, noise: Optional[float] = 0.01, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    thoughts = find(content, model, relatedness,
                    serendipity, noise, silent, top_k)
    return PlainTextResponse(plaintext_response(thoughts))


@app.get('/find/lang/file')
async def find_by_language_return_file(content: str, relatedness: Optional[float] = 1, serendipity: Optional[float] = 0, noise: Optional[float] = 0.01, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    thoughts = find(content, model, relatedness,
                    serendipity, noise, silent, top_k)
    return FileResponse(file_response(thoughts))


@app.get('/find/lang/json')
async def find_by_language_return_json(content: str, relatedness: Optional[float] = 1, serendipity: Optional[float] = 0, noise: Optional[float] = 0.01, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    thoughts = find(content, model, relatedness,
                    serendipity, noise, silent, top_k)
    return json_response(thoughts)


@app.post('/find/imag/html')
async def find_by_imagery_return_html(file: UploadFile = File(...), relatedness: Optional[float] = 1, serendipity: Optional[float] = 0, noise: Optional[float] = 0.01, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    content = await file.read()
    thoughts = find(content, model, relatedness,
                    serendipity, noise, silent, top_k)
    return HTMLResponse(html_response(thoughts))


@app.post('/find/imag/text')
async def find_by_imagery_return_plaintext(file: UploadFile = File(...), relatedness: Optional[float] = 1, serendipity: Optional[float] = 0, noise: Optional[float] = 0.01, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    content = await file.read()
    thoughts = find(content, model, relatedness,
                    serendipity, noise, silent, top_k)
    return PlainTextResponse(plaintext_response(thoughts))


@app.post('/find/imag/file')
async def find_by_imagery_return_file(file: UploadFile = File(...), relatedness: Optional[float] = 1, serendipity: Optional[float] = 0, noise: Optional[float] = 0.01, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    content = await file.read()
    thoughts = find(content, model, relatedness,
                    serendipity, noise, silent, top_k)
    return FileResponse(file_response(thoughts))


@app.post('/find/imag/json')
async def find_by_imagery_return_json(file: UploadFile = File(...), relatedness: Optional[float] = 1, serendipity: Optional[float] = 0, noise: Optional[float] = 0.01, silent: Optional[bool] = False, top_k: Optional[int] = 50):
    content = await file.read()
    thoughts = find(content, model, relatedness,
                    serendipity, noise, silent, top_k)
    return json_response(thoughts)


@app.get('/rset/embs')
async def reset_embeddings_handle():
    reset_embeddings(model)


@app.get('/dump')
async def dump_conceptarium():
    return FileResponse(archive_response(), filename='conceptarium.zip')
