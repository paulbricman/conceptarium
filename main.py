from fastapi import FastAPI, File

from util import *

app = FastAPI()
model = load_model()
init()


@app.get("/add/text")
async def add_text_thought_handler(text: str):
    add_thought(Thought(text, model))


@app.post("/add/image")
async def add_image_thought_handler(file: bytes = File(...)):
    add_thought(Thought(file, model))


@app.get("/get/text")
async def get_thought_handler(text: str):
    return get_thoughts(text, model)


@app.post("/get/image")
async def get_thought_handler(file: bytes = File(...)):
    return get_thoughts(file, model)
