
 # служебка

from database import finance_db
from datetime import datetime


  # сбор всей информации для интерфейса
async def get_all_data(filters=None):
    db = await finance_db.get_db()
    await finance_db.ensure_categories()

    #await finance_db.recalculate_balances()
    
    transactions = await finance_db.get_transactions(filters)
    for t in transactions:
        t.date_str = t.date.strftime("%d.%m.%Y %H:%M")

    accounts = await finance_db.get_accounts()
    categories = await db.categories.find().to_list(100)

    start_of_month = datetime(datetime.now().year, datetime.now().month, 1)
    monthly = await db.transactions.aggregate([
        {"$match": {"type": "expense", "date": {"$gte": start_of_month}}},
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
        {"$sort": {"total": -1}}
    ]).to_list(100)

    return {
        "transactions": transactions,
        "accounts": accounts,
        "categories": categories,
        "monthly_expenses": monthly,
    }
























# from datetime import datetime
# from database import wait_for_mongo


# #  возвращает объект базы данных
# async def get_db():
#     return await wait_for_mongo()


# # пересчет балансов (вызывается после операций добавления и удаления расходов)
# async def recalc_all_balances(db):
#     pipeline = [
#         {"$group": {
#             "_id": "$account",
#             "balance": {
#                 "$sum": {
#                     "$cond": [{"$eq": ["$type", "income"]}, "$amount", {"$multiply": ["$amount", -1]}]
#                 }
#             }
#         }}
#     ]
#     #  получаем список результатов
#     result = await db.transactions.aggregate(pipeline).to_list(None)

#     #  обновление балансов
#     for r in result:
#         await db.accounts.update_one(
#             {"name": r["_id"]},
#             {"$set": {"balance": r["balance"]}},
#             upsert=True
#         )

# # получает все данные со страницы
# async def get_all_data(db, filters=None):
#     if filters is None:
#         filters = {}

#     # Транзакции
#     transactions = [
#         t async for t in db.transactions.find(filters).sort("date", -1)
#     ]
#     for t in transactions:
#         t["id"] = str(t["_id"])
#         t["date_str"] = t["date"].strftime("%d.%m.%Y %H:%M")

#     # Счета
#     accounts = [a async for a in db.accounts.find()]

#     # Категории (с дефолтными)
#     categories = await db.categories.find().to_list(100)
#     if not categories:
#         default = [
#             {"name": "Зарплата", "type": "income"},
#             {"name": "Еда", "type": "expense"},
#             {"name": "Транспорт", "type": "expense"},
#             {"name": "Коммуналка", "type": "expense"},
#         ]
#         await db.categories.insert_many(default)
#         categories = default

#     # Расходы за месяц
#     start_of_month = datetime(datetime.now().year, datetime.now().month, 1)
#     monthly = await db.transactions.aggregate([
#         {"$match": {"type": "expense", "date": {"$gte": start_of_month}}},
#         {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
#         {"$sort": {"total": -1}}
#     ]).to_list(100)

#     return {
#         "transactions": transactions,
#         "accounts": accounts or [],
#         "categories": categories,
#         "monthly_expenses": monthly,
#     }