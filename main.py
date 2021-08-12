from fastapi import FastAPI, File

app = FastAPI()


@app.get("/add/text")
async def add_text_thought(text: str):
    return "ok"


@app.post("/add/image")
async def add_image_thought(file: bytes = File(...)):
    return "ok"
