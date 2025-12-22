

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from database import finance_db
from operations import get_all_data
from frontend import draw_page

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, account: str | None = None, type: str | None = None, category: str | None = None):
    filters = {}
    if account: filters["account"] = account
    if type: filters["type"] = type
    if category: filters["category"] = category

    data = await get_all_data(filters)
    html = draw_page(data, request)
    return HTMLResponse(html)

@app.post("/add_account")
async def add_account(name: str = Form(...)):
    await finance_db.add_account(name)
    return RedirectResponse("/", status_code=303)

@app.post("/add_transaction")
async def add_transaction(
    account: str = Form(...),
    category: str = Form(...),
    amount: float = Form(...),
):
    db = await finance_db.get_db()
    
    # Находим категорию, чтобы узнать тип (income или expense)
    cat_doc = await db.categories.find_one({"name": category})
    if not cat_doc:
        # Если категории нет — ошибка, но  все категории есть по умолчанию
        return HTMLResponse("Категория не найдена", status_code=400)
    
    transaction_type = cat_doc["type"]  # "income" или "expense"
    
    await finance_db.add_transaction(account, category, amount, transaction_type)
    return RedirectResponse("/", status_code=303)


@app.get("/delete/{transaction_id}")
async def delete_transaction(transaction_id: str):
    await finance_db.delete_transaction(transaction_id)
    return RedirectResponse("/", status_code=303)


@app.get("/delete_account/{account_name}")
async def delete_account_route(account_name: str):
    """Обработчик нажатия на крестик у счёта"""
    success = await finance_db.delete_account(account_name)
    
    return RedirectResponse("/", status_code=303)

@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    account: str | None = None,
    category: str | None = None,
):
    filters = {}
    if account:
        filters["account"] = account
    if category:
        filters["category"] = category

    data = await get_all_data(filters)
    html = draw_page(data)
    return HTMLResponse(html)

















# # main.py основной файл с конфигурацией 
# from fastapi import FastAPI, Form, Request
# from fastapi.responses import HTMLResponse, RedirectResponse
# from operations import get_db, recalc_all_balances, get_all_data
# from frontend import draw_page 
# from datetime import datetime

# app = FastAPI()

# @app.get("/", response_class=HTMLResponse)
# async def index(
#     request: Request,                       #
#     account: str | None = None,             # фильтр по счету
#     type: str | None = None,                # фильтр по типу
#     category: str | None = None,            # фильтр по категрии
# ):
#     db = await get_db()  # подключение к бд # async bkb ytn
#     filters = {}
#     if account: filters["account"] = account
#     if type: filters["type"] = type
#     if category: filters["category"] = category

#     data = await get_all_data(db, filters) # полный сбор данных
#     html = draw_page(data)               # генераци страницы
#     return HTMLResponse(html)              

# # добавление счета
# @app.post("/add_account")
# async def add_account(name: str = Form(...)): # обязательное имя
#     db = await get_db()
#     await db.accounts.insert_one({"name": name, "balance": 0.0}) # созжание пустого счета 
#     return RedirectResponse("/", status_code=303)

# # создание тразакции
# @app.post("/add_transaction")
# async def add_transaction(
#     account: str = Form(...),       # счет
#     category: str = Form(...),      
#     amount: float = Form(...),      # сумма
#     type: str = Form(...),          #  тип - расход или доход
# ):
#     db = await get_db()

#     await db.transactions.insert_one({ #  добаввление в БД
#         "account": account,
#         "category": category,
#         "amount": amount,
#         "type": type,
#         "date": datetime.utcnow(),
#     })
#     await recalc_all_balances(db)      # пересчет баланса
#     return RedirectResponse("/", status_code=303)
