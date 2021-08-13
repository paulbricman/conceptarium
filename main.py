from fastapi import FastAPI, File
from fastapi.datastructures import UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse
import secrets
from pathlib import Path

from util import *
from responses import *

app = FastAPI()
model = load_model()
init()

app.mount("/conceptarium", StaticFiles(directory="conceptarium"))


@app.get("/mem/language")
async def memorize_language(content: str):
    filename = 'conceptarium/' + secrets.token_urlsafe(8) + '.txt'
    open(filename, 'w').write(content)
    memorize(Thought(filename, content, model))


@app.post("/mem/imagery")
async def memorize_imagery(file: UploadFile = File(...)):
    content = await file.read()
    extension = Path(file.filename).suffix
    filename = 'conceptarium/' + \
        secrets.token_urlsafe(8) + extension
    open(filename, 'wb+').write(content)
    memorize(Thought(filename, content, model))


@app.get("/rem/language/html")
async def remember_by_language_via_html(content: str, behavior: str, top_k: int = 50):
    print('HANDLER BEHAVIOR', behavior)
    thoughts = remember(content, model, behavior, top_k)
    return HTMLResponse(html_response(thoughts))


@app.get("/rem/language/plaintext")
async def remember_by_language_via_plaintext(content: str, behavior: str, top_k: int = 50):
    thoughts = remember(content, model, behavior, top_k)
    return PlainTextResponse(plaintext_response(thoughts))


@app.get("/rem/language/file")
async def remember_by_language_via_file(content: str, behavior: str, top_k: int):
    thoughts = remember(content, model, behavior, top_k)
    return FileResponse(file_response(thoughts))


@app.get("/rem/language/json")
async def remember_by_language_via_json(content: str, behavior: str, top_k: int):
    thoughts = remember(content, model, behavior, top_k)
    return json_response(thoughts)


@app.post("/rem/imagery/html")
async def remember_by_imagery_via_html(file: UploadFile = File(...), behavior: str = 'balanced', top_k: int = 50):
    content = await file.read()
    thoughts = remember(content, model, behavior, top_k)
    return HTMLResponse(html_response(thoughts))


@app.post("/rem/imagery/plaintext")
async def remember_by_imagery_via_plaintext(file: UploadFile = File(...), behavior: str = 'balanced', top_k: int = 50):
    content = await file.read()
    thoughts = remember(content, model, behavior, top_k)
    return PlainTextResponse(plaintext_response(thoughts))


@app.post("/rem/imagery/file")
async def remember_by_imagery_via_json(file: UploadFile = File(...), behavior: str = 'balanced', top_k: int = 50):
    content = await file.read()
    thoughts = remember(content, model, behavior, top_k)
    return FileResponse(file_response(thoughts))


@app.post("/rem/imagery/json")
async def remember_by_imagery_via_json(file: UploadFile = File(...), behavior: str = 'balanced', top_k: int = 50):
    content = await file.read()
    thoughts = remember(content, model, behavior, top_k)
    return json_response(thoughts)
