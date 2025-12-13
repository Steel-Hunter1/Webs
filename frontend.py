 # отрисовка страички  HTML 
def draw_page(data: dict, request = None) -> str:
    with open("templates/index.html", encoding="utf-8") as f:
        html = f.read()

    trans_rows = ""
    for t in data["transactions"]:
        color = "green" if t.type == "income" else "red"
        sign = "+" if t.type == "income" else "-"
        # Добавляем кнопку удаления (крестик)
        delete_btn = f'<a href="/delete/{t.id}" style="color:red; text-decoration:none; margin-left:10px;" onclick="return confirm(\'Удалить эту транзакцию?\')">✕</a>'
        trans_rows += f"""
        <tr>
            <td>{t.date_str}</td>
            <td>{t.account}</td>
            <td>{t.category}</td>
            <td style="color:{color};text-align:right">{sign}{t.amount:.2f}</td>
            <td>{'Доход' if t.type=='income' else 'Расход'}</td>
            <td>{delete_btn}</td>
        </tr>
        """

    # Выделение счета
    account_options = ""
    for a in data["accounts"]:
        selected = ' selected' if a.name == request.query_params.get("account") else ''
        account_options += f'<option value="{a.name}"{selected}>{a.name}</option>'

    # Выделение категории
    cat_options = ""
    for c in data["categories"]:
        selected = ' selected' if c["name"] == request.query_params.get("category") else ''
        cat_options += f'<option value="{c["name"]}"{selected}>{c["name"]}</option>'

    # Таблица счетов
    account_list = ""
    for a in data["accounts"]:
        bal = a.balance
        color = "green" if bal >= 0 else "red"
        
        delete_btn = ""
        
        delete_btn = f'<a href="/delete_account/{a.name}" style="color:red; margin-left:10px;" onclick="return confirm(\'Удалить счёт «{a.name}» и все его транзакции?\')">Remove</a>'
        

        account_list += f"""
        <tr>
            <td>{a.name}{delete_btn}</td>
            <td style='color:{color};text-align:right'>{bal:.2f} ₽</td>
        </tr>
        """

    monthly_rows = ""
    for m in data["monthly_expenses"]:
        monthly_rows += f"<tr><td>{m['_id']}</td><td style='text-align:right'>{m['total']:.2f} ₽</td></tr>"

    html = html.replace("{{TRANSACTIONS}}", trans_rows)
    html = html.replace("{{ACCOUNT_OPTIONS}}", account_options)
    html = html.replace("{{CATEGORY_OPTIONS}}", cat_options)
    html = html.replace("{{ACCOUNT_LIST}}", account_list)
    html = html.replace("{{MONTHLY_EXPENSES}}", monthly_rows)

    return html















# # frontend.py
# def render_page(data: dict) -> str:
#     with open("templates/index.html", encoding="utf-8") as f:
#         html = f.read()

#     # Транзакции
#     trans_rows = ""
#     for t in data["transactions"]:
#         color = "green" if t["type"] == "income" else "red"
#         sign = "+" if t["type"] == "income" else "-"
#         trans_rows += f"""
#         <tr>
#             <td>{t['date_str']}</td>
#             <td>{t['account']}</td>
#             <td>{t['category']}</td>
#             <td style="color:{color};text-align:right">{sign}{t['amount']:.2f}</td>
#             <td>{'Доход' if t['type']=='income' else 'Расход'}</td>
#         </tr>
#         """

#     # Опции для форм
#     account_options = "".join(f'<option value="{a["name"]}">{a["name"]}</option>' for a in data["accounts"])
#     cat_options = "".join(f'<option value="{c["name"]}">{c["name"]}</option>' for c in data["categories"])

#     # Счета
#     account_list = ""
#     for a in data["accounts"]:
#         bal = a.get("balance", 0)
#         color = "green" if bal >= 0 else "red"
#         account_list += f"<tr><td>{a['name']}</td><td style='color:{color};text-align:right'>{bal:.2f} ₽</td></tr>"

#     # Расходы за месяц
#     monthly_rows = ""
#     for m in data["monthly_expenses"]:
#         monthly_rows += f"<tr><td>{m['_id']}</td><td style='text-align:right'>{m['total']:.2f} ₽</td></tr>"

#     # Подстановка
#     html = html.replace("{{TRANSACTIONS}}", trans_rows)
#     html = html.replace("{{ACCOUNT_OPTIONS}}", account_options)
#     html = html.replace("{{CATEGORY_OPTIONS}}", cat_options)
#     html = html.replace("{{ACCOUNT_LIST}}", account_list)
#     html = html.replace("{{MONTHLY_EXPENSES}}", monthly_rows)

#     return html