from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request" : request})

@app.post("/generate")
async def generate_text(model: str = Form(), prompt: str = Form()):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt},
        )
        response_lines = response.text.split("\n")
        response_objects = [json.loads(line) for line in response_lines if line]

        response_text = ''.join([obj['response'] for obj in response_objects])

        return response_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


