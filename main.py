from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import urllib.parse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database Connection (Replace with your credentials)
username = urllib.parse.quote_plus("s-md-ahmed")
password = urllib.parse.quote_plus("test123")
uri = f"mongodb+srv://{username}:{password}@cluster0.izqpyt7.mongodb.net/"
conn = MongoClient(uri)

# Fetch documents from the "notes" collection
cursor = conn.notes.notes.find({})  # Use find() to retrieve multiple documents
new_docs = []
for document in cursor:
    new_doc = {
        "id": str(document["_id"]),  # Convert ObjectId to string for Jinja
        "note": document.get("note", "")  # Handle missing "note" field
    }
    new_docs.append(new_doc)
print(new_docs)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "notes": new_docs})
