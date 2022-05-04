import sqlite3
import requests

try:
    sqlite_connection = sqlite3.connect('sqlite_python.db')       #выполняется полключение к бд
    cursor = sqlite_connection.cursor()                           #Объект, который позволяет выполнять SQL-запросы из Python
    print("База данных создана и успешно подключена к SQLite")

    sqlite_select_query = "select sqlite_version();"              #метод execute, с помощью корого можно выполнить запрос в бд из Python.
    cursor.execute(sqlite_select_query)                           #он принимает SQL-запрос в кач-ве пар-ра и возвращает resultSet — то есть, строки базы данных
    record = cursor.fetchall()                                    # Получить результат запроса из resultSet можно с помощью методов, например, fetchAll()
    print("Версия базы данных SQLite: ", record)

    #получаем количество таблиц с названием questions
    cursor.execute('''SELECT count(name) FROM sqlite_master where type ='table' AND name = 'questions' ''')

    #если их количество равно 1, то таблица существует
    if cursor.fetchone()[0] == 1:
        print("Таблица questions существует")
    else:
        create_table_questions = '''CREATE TABLE questions (
                                group_id INTEGER,
                                group_name TEXT,
                                question_id INTEGER,
                                question TEXT,
                                answer TEXT);'''
        cursor.execute(create_table_questions)
        print("Таблица questions создана")
        sqlite_connection.commit()

    # обращаемся к эндпоинту /api/random публичного API сервиса https://jservice.io/
    res = requests.get("https://jservice.io/api/random")
    #print(res.status_code)
    json = res.json()
    a = (json[0]['category']['id'], json[0]['category']['title'], json[0]['id'], json[0]['question'], json[0]['answer'])

    #запись в бд
    cursor.execute('''INSERT INTO questions 
                                    (group_id, group_name, question_id, question, answer)
                                    VALUES (?, ?, ?, ?, ?)''', a)
    sqlite_connection.commit()     #сохраняем изменения
    print("Информация записана в базу данных")

    #вывод данных из бд в консоль
    print()
    print("Вывод данных")
    cursor.execute("SELECT* FROM questions ORDER BY group_id, question_id")
    while True:
        row = cursor.fetchone()
        if row == None:
            break
        print(row[0], row[2], row[1], row[3], row[4], sep=', ')

    cursor.close()

except sqlite3.Error as error:                                    #Класс sqlite3.Error позволит понять суть ошибки. Он возвращает сообщение и код ошибки.
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")
