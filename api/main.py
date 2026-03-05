from fastapi import FastAPI, HTTPException
from pathlib import Path
import json

app = FastAPI(title="Demo API JSON")

DATA_PATH = Path(__file__).resolve().parent.parent / "data.json"

def load_data():
    if not DATA_PATH.exists():
        return []
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/people")
def people():
    return load_data()

@app.get("/person/{person_id}")
def person(person_id: str):
    data = load_data()
    found = next((x for x in data if str(x.get("id")) == str(person_id)), None)
    if not found:
        raise HTTPException(status_code=404, detail="ID no encontrado")
    return found
