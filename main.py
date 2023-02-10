from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3, config
from datetime import date
import numpy as np

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    stock_filter = request.query_params.get('filter', False)
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if stock_filter == 'new_closing_highs':
        cursor.execute("""
        SELECT * FROM (
            SELECT symbol, name, stock_id, max(close), date FROM stock_price JOIN stock 
            ON stock.id = stock_price.stock_id GROUP BY stock_id ORDER BY symbol
        ) WHERE date = ?
        """, (date.today().isoformat(),))
    elif stock_filter == 'new_closing_lows':
        cursor.execute("""
        SELECT * FROM (
            SELECT symbol, name, stock_id, min(close), date FROM stock_price JOIN stock 
            ON stock.id = stock_price.stock_id GROUP BY stock_id ORDER BY symbol
        ) WHERE date = ?
        """, (date.today().isoformat(),))
    else:
        cursor.execute("""
            SELECT id, symbol, name FROM stock ORDER BY symbol
        """)

    rows = cursor.fetchall()

    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})


@app.get("/account_info")
def account_info(request: Request):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Selecting info
    account_data = cursor.execute("""
        SELECT date, portfolio_value, cash, buying_power FROM account_info
    """)
    account_data2 = account_data.fetchall()

    dates = [row['date'] for row in account_data2]
    portfolio_values = [row['portfolio_value'] for row in account_data2]
    dates = np.array(dates)
    portfolio_values = np.array(portfolio_values)

    for row in account_data2:
        print(row['date'], row['portfolio_value'], row['cash'], row['buying_power'])
    return templates.TemplateResponse("account_info.html", {"request": request,
                                      "rows": account_data2})


@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM strategy
    """)
    strategies = cursor.fetchall()

    cursor.execute("""
        SELECT id, symbol, name FROM stock WHERE symbol = ?
    """, (symbol,))
    row = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date DESC
    """, (row['id'],))
    prices = cursor.fetchall()

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
