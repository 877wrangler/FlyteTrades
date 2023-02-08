from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import sqlite3, config

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, symbol, name FROM stock 
    """)

    rows = cursor.fetchall()

    return templates.TemplateResponse("index.html", {"request": request, "id": id})

    return {"Hello": "World", "stocks": rows}