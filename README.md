# Webs
My task for this year
Проект финансового приложения

Данное приложение предназначено для учета какого-либо бюджета (личного, семейного, предприятия и т.д.), который представляет из себя один или несколько счетов. 

Взаимодействие со счетами происходит посредством добавления или удаления транзакций (операции со счетом), которые подразделяются на категории, которые имеют атрибут дохода или расхода. После каждого действия со счетами балансы пересчитываются, чтобы сохранять актуальную сумму на балансе.

	Запуск приложения
Для запуска приложения необходимо:
1.	Собрать все необходимые файлы
2.	Расположить все файлы согласно схеме:
…/personal-finance
.....->main.py
.....->database.py
.....->frontend.py
.....->operations.py
.....->dockerfile
.....->docker-compose.yml
.....->requirements.txt
.....->/templates/index.html
3.	Открыть терминал внутри директории 
4.	Набрать команду (sudo) docker compose up –build и немного подождать
5.	В браузерной строке набрать http://localhost и перейти
6.	В браузере должно появиться приложение следующего вида:  
<img width="766" height="433" alt="image" src="https://github.com/user-attachments/assets/7f34baf8-baff-432e-b288-df9ae339e74b" />



Инструкция для пользователя
Создание и удаление счета
Для создания счета введите его название в графу «название счета» и нажмите «Создать счет».  <img width="913" height="325" alt="image" src="https://github.com/user-attachments/assets/1c1b557f-1eec-48c2-9044-04ecb03091ed" />
 После этого в таблице счетов появится только что созданный счет с нулевым балансом
 <img width="974" height="127" alt="image" src="https://github.com/user-attachments/assets/22fe48eb-055a-40be-a212-e7f5c7df1069" />




Для удаления счета перейдите к таблице счетов и найдите счет, который вы хотите удалить. 
 <img width="974" height="151" alt="image" src="https://github.com/user-attachments/assets/1c68bb1a-248b-4d71-ae85-d3a3b1264bd1" />

Убедитесь, что все транзакции этого счета не представляют интереса, поскольку при удалении счета удалятся ВСЕ его транзакции.   
<img width="974" height="149" alt="image" src="https://github.com/user-attachments/assets/bfd81db6-da42-48aa-993e-a04efd85bc55" />

Нажмите кнопку «Удалить счет» и подтвердите.
 <img width="859" height="265" alt="image" src="https://github.com/user-attachments/assets/0032cb9f-ec4f-48cd-9d63-a22a4faf96e2" />
<img width="817" height="266" alt="image" src="https://github.com/user-attachments/assets/762d6f0c-324c-4a2a-91f1-cfa5a9a88a79" />


Добавление и удаление транзакции
Для добавления транзакции нужно перейти в раздел «Новая операция»
<img width="974" height="154" alt="image" src="https://github.com/user-attachments/assets/edd5ff75-1ae6-4a99-8618-7721297f688e" />

Выберете счет, с которым вы будите взаимодействовать. Укажите категорию операции и сумму. Затем нажмите кнопку «добавить»  
 <img width="974" height="94" alt="image" src="https://github.com/user-attachments/assets/c4f60f34-b9fd-440c-93aa-17307da31269" />



Чтобы удалить транзакцию, нужно нажать значок крестика и подтвердить
  <img width="974" height="94" alt="image" src="https://github.com/user-attachments/assets/c98423e1-47a1-4ea0-b601-99a903ab060a" />
<img width="817" height="243" alt="image" src="https://github.com/user-attachments/assets/5cfb9b55-9b41-4091-a1c2-4d7598cbb3cc" />
<img width="974" height="107" alt="image" src="https://github.com/user-attachments/assets/f0034665-f328-4b38-bdfd-eb40ad61313e" />

 
Использование фильтров
Для того, чтобы отсмотреть транзакции по какому-либо критерию, перейдите в раздел фильтры, настройте критерии отбора и нажмите «применить». После этого таблица с операциями оставит в себе только интересующие вас данные   <img width="974" height="190" alt="image" src="https://github.com/user-attachments/assets/c437a8ce-a965-4832-9e48-0fd50551123d" />
<img width="974" height="495" alt="image" src="https://github.com/user-attachments/assets/0cf34e15-6590-4417-9910-dbc7afca4d17" />
<img width="974" height="129" alt="image" src="https://github.com/user-attachments/assets/2a01209c-ea6c-4dae-9d03-0e9ec3aad7df" />

