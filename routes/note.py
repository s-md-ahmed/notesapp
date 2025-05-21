from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from config.db import conn  # Assuming this is your database connection file

# Create an APIRouter instance
note = APIRouter()

# Set up Jinja2 templating engine
templates = Jinja2Templates(directory="templates")

# Retrieve all documents (notes) from the "notes" collection
cursor = conn.notes.notes.find({})
new_docs = []

# Process each retrieved document
for document in cursor:
    new_doc = {
        "id": str(document["_id"]),
        "title": document.get("title", ""),
        "desc": document.get("desc", ""),
        "important": document.get("important", "")
    }
    new_docs.append(new_doc)

# Define a GET route for the root path ("/")
@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    """Renders the 'index.html' template with the list of notes."""
    return templates.TemplateResponse("index.html", {"request": request, "notes": new_docs})

# Define a POST route for the root path ("/")
@note.post("/")
async def postreq(request: Request):
    """Handles form submission for creating new notes."""
    form = await request.form()
    formDict = dict(form)

    # Handle 'important' checkbox
    if "important" in formDict:
        formDict["important"] = True if formDict["important"] == "on" else False
    else:
        formDict["important"] = False

    # Insert the new note into the database
    conn.notes.notes.insert_one(formDict)

    # Render 'tq.html' template
    return templates.TemplateResponse("tq.html", {"request": request})
@note.put("/notes/{id}")
async def update_note(id: str, request: Request):
    updated_data = await request.json()