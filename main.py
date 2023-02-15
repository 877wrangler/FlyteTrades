from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3, config
from account_info import account_status
from stock_list import stock_list
from stock_detail import daily_stock_data

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    stock_filter = request.query_params.get('filter', False)
    rows = stock_list(stock_filter)
    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})


@app.get("/account_info")
def account_info(request: Request):
    fig_json, account_data2 = account_status()
    return templates.TemplateResponse("account_info.html", {"request": request, "fig_json": fig_json,
                                                            "rows": account_data2})


@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol):
    row, prices, strategies = daily_stock_data(symbol)
    return templates.TemplateResponse("stock_detail.html",
                                      {"request": request, "stock": row, "bars": prices, "strategies": strategies})


@app.post("/apply_strategy")
def apply_strategy(strategy_id: int = Form(...), stock_id: int = Form(...)):
    connection = sqlite3.connect(config.DB_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (?, ?)
    """, (stock_id, strategy_id))

    connection.commit()

    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)


@app.get("/strategy/{strategy_id}")
def strategy(request: Request, strategy_id):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name FROM strategy WHERE id = ?
    """, (strategy_id,))

    strategy = cursor.fetchone()

    cursor.execute("""
        SELECT symbol, name FROM stock
        JOIN stock_strategy on stock_strategy.stock_id = stock.id
        WHERE strategy_id = ?
    """, (strategy_id,))

    stocks = cursor.fetchall()

    return templates.TemplateResponse("strategy.html", {"request": request, "stocks": stocks, "strategy": strategy})
