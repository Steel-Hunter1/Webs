from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import asyncio
import os
from datetime import datetime
from typing import List, Optional
class Account: # класс со счетом
    
    def __init__(self, name: str, balance: float = 0.0):
        self.name = name
        self.balance = balance
    def to_dict(self):
        # возвращает списком данные о счете, чтобы вставлять в БД
        return {"name": self.name, "balance": self.balance}
    
class Transaction: 
    def __init__(self, account: str, category: str, amount: float, type_: str, date: datetime, _id = None):
        self.id = str(_id) if _id else None # ID
        self.account = account              # счет 
        self.category = category            # категория
        self.amount = amount                # сумма
        self.type = type_                   # income или expense
        self.date = date                    # дата и время
    
    # возвращает списком данные о счете, чтобы вставлять в БД
    def to_dict(self):
        data = { 
            "account": self.account,
            "category": self.category,
            "amount": self.amount,
            "type": self.type,
            "date": self.date
        }
        return data


class FinanceDB:
    # инкапсулирующий класс для базы данных
    def __init__ (self):
        self.client = None
        self.db = None

    # подключение к mongodb 
    async def connect(self):
        url = "mongodb://mongo:27017/finance"
        for _ in range (30):
            try:
                self.client = AsyncIOMotorClient(url, serverSelectionTimeoutMS = 1000)
                await self.client.admin.command("ping")
                print("MongoDB подключен!")
                self.db = self.client.finance
                return
            except:
                print ("Ожидание MongoDB...")
                await asyncio.sleep(1)
            raise Exception("Не удалось подключиться к MongoDB")
        
        
    async def get_db(self):
        # возвращает объект базы
        if self.db is None:
            await self.connect()
        return self.db
    
     # добавить счет 
    async def add_account(self, name: str): 
        db = await self.get_db() 
        account = Account (name)
        await db.accounts.insert_one(account.to_dict())
        await self.recalculate_balances()

    # узнает о всех счетах с их балансами
    async def get_accounts(self) -> List[Account]:
        db = await self.get_db()
        accounts = []
        async for doc in db.accounts.find():
            balance = doc.get("balance", 0.0)
            print(f"Счет из бд: {doc['name']} — баланс {balance}")
            accounts.append(Account(doc["name"], balance))
        return accounts
    
      # удаляет счет и всю его историю (транзации)
    async def delete_account(self, account_name: str):
        
        db = await self.get_db()
        
        # удаление транзакций у счета 
        await db.transactions.delete_many({"account": account_name})
        
        # удаление самомго счета 
        result = await db.accounts.delete_one({"name": account_name})
        await self.recalculate_balances()
        # в результат отправляем успех или неуспех удаления
        return result.deleted_count > 0

    #======================================================================
    # добавление транзакции 
    async def add_transaction(self, account: str, category: str, amount: float, type_: str):
        db = await self.get_db()
        transaction = Transaction(account, category, amount, type_, datetime.utcnow())
        await db.transactions.insert_one(transaction.to_dict())
        print (f"добавлена транзакция: {type_} {amount} на счет {account}")
        await self.recalculate_balances()
 
    # удаление транзакции
    async def delete_transaction(self, transaction_id: str):
        db = await self.get_db()
        result = await db.transactions.delete_one({"_id": ObjectId(transaction_id)})
        if result.deleted_count > 0:
            await self.recalculate_balances()
            return True
        return False
    
      # выдает спиком транзакции с фильтром(ми)
    async def get_transactions (self, filters = None) -> List[Transaction]:
        if filters is None:
            filters = {}
        db = await self.get_db()
        transactions = []
        async for doc in db.transactions.find(filters).sort("date", -1):
            transactions.append(Transaction(
                doc["account"], 
                doc["category"],
                doc["amount"],
                doc["type"],
                doc["date"],
                doc["_id"]
            )
                                )
        return transactions 
    
        # обновляет баланс счетов (используется сразу после добавления или удаления транзакций)
    async def recalculate_balances(self):
        
        db = await self.get_db()
        
        # получение всех счетов
        accounts = [doc async for doc in db.accounts.find({}, {"name": 1})]
        
        # Для каждого счёта считаем баланс заново
        for acc in accounts:
            account_name = acc["name"]
            
            # Для всех счетов: берет счет и прибавляет доходы и вычитает расходы
            pipeline = [
                {"$match": {"account": account_name}},
                {
                    "$group": {
                        "_id": None,
                        "total": {
                            "$sum": {
                                "$cond": [
                                    {"$eq": ["$type", "income"]},
                                    "$amount",
                                    {"$multiply": ["$amount", -1]}
                                ]
                            }
                        }
                    }
                }
            ]
            result = await db.transactions.aggregate(pipeline).to_list(1)
            new_balance = result[0]["total"] if result else 0.0
            
            # обновляет баланс в базе
            await db.accounts.update_one(
                {"name": account_name},
                {"$set": {"balance": new_balance}}
            )
            print(f"Счёт '{account_name}' обновлён: баланс = {new_balance}")
        print("Балансы пересчитаны!")

    # async def recalculate_balances(self):
    #     db = await self.get_db()
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
    #     result = await db.transactions.aggregate(pipeline).to_list(None)
    #     for r in result:
    #         await db.accounts.update_one(
    #             {"name": r["_id"]},
    #             {"$set": {"balance": r["balance"]}},
    #             upsert = True
    #         )

    # создает категрии с их типами
    async def ensure_categories(self):
        
        db = await self.get_db()
        count = await db.categories.count_documents({})
        if count == 0:
            default = [
                {"name": "Зарплата", "type": "income"},
                {"name": "Прочие доходы", "type": "income"},
                
                {"name": "Еда", "type": "expense"},
                {"name": "Транспорт", "type": "expense"},
                {"name": "Коммуналка", "type": "expense"},
                {"name": "Прочие расходы", "type": "expense"},
                {"name": "Перевод", "type": "expense"},
                {"name": "Накопления", "type": "expense"},
            ]
            await db.categories.insert_many(default)


finance_db = FinanceDB()






# # ожидание поднятия  mongo 
# async def wait_for_mongo():

#     url = os.getenv("MONGODB_URL", "mongodb://mongo:27017/finance")
#     for _ in range(30): 
#         try:  # раз в секунду аытаемся  подключиться
#             client = AsyncIOMotorClient(url, serverSelectionTimeoutMS=1000)
#             await client.admin.command("ping")
#             print("MongoDB подключён!")
#             return client.finance
#         except Exception:
#             print("Ожидание MongoDB...")
#             await asyncio.sleep(1)
#     raise Exception("Не удалось подключиться к MongoDB за 30 секунд")




    

