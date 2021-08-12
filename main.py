from fastapi import FastAPI, File
from fastapi.datastructures import UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, PlainTextResponse
import secrets
from pathlib import Path

from util import *

app = FastAPI()
model = load_model()
init()

app.mount("/conceptarium", StaticFiles(directory="conceptarium"))


@app.get("/add/language")
async def add_language_handler(content: str):
    filename = 'conceptarium/' + secrets.token_urlsafe(8) + '.txt'
    open(filename, 'w').write(content)
    attach_metadata(Thought(filename, content, model))


@app.post("/add/imagery")
async def add_image_thought_handler(file: UploadFile = File(...)):
    content = await file.read()
    extension = Path(file.filename).suffix
    filename = 'conceptarium/' + \
        secrets.token_urlsafe(8) + extension
    open(filename, 'wb+').write(content)
    attach_metadata(Thought(filename, content, model))


@app.get("/get/language/html")
async def get_thought_html_handler(content: str):
    thoughts = get_thoughts(content, model)
    return HTMLResponse(html_response(thoughts))


@app.get("/get/language/plaintext")
async def get_thought_plaintext_handler(content: str):
    thoughts = get_thoughts(content, model)
    return PlainTextResponse(plaintext_response(thoughts))
