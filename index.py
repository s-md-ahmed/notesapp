from fastapi import FastAPI
from routes.note import note
from fastapi.templating import Jinja2Templates
app=FastAPI()
app.include_router(note)
templates = Jinja2Templates(directory="templates")