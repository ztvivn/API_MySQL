from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import time  # Добавляем импорт для функции ожидания

# Создаем экземпляр Flask-приложения
app = Flask(__name__)

# Настройки подключения к базе данных MySQL из переменных окружения
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Берем значение из переменной окружения или используем 'localhost'
    'user': os.getenv('DB_USER', 'user_name'),  # Пользователь
    'password': os.getenv('DB_PASSWORD', 'password123'),  # Пароль
    'database': os.getenv('DB_NAME', 'mail_database')  # Название базы данных
}

# Функция ожидания готовности базы данных
def wait_for_mysql():
    while True:
        try:
            connection = mysql.connector.connect(**db_config)
            if connection.is_connected():
                print("Успешное подключение к MySQL")
                connection.close()
                break
        except mysql.connector.Error:
            print("Ожидание подключения к MySQL...")
            time.sleep(2)

# Вызываем функцию перед запуском Flask
wait_for_mysql()

# Главная страница, отображающая данные из таблиц
@app.route('/')
def index():
    try:
        # Подключаемся к базе данных
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Извлекаем данные из таблицы "organization_addresses"
        cursor.execute("SELECT organization_name, address, director_lastname FROM organization_addresses")
        organization_records = cursor.fetchall()  # Сохраняем записи организаций

        # Извлекаем данные из таблицы "correspondence"
        cursor.execute("SELECT correspondence_type, preparation_date, organization_name FROM correspondence")
        correspondence_records = cursor.fetchall()  # Сохраняем записи корреспонденции

    except mysql.connector.Error as e:
        # Если произошла ошибка при подключении, выводим её в консоль
        print(f"Ошибка подключения к базе данных: {e}")
        organization_records = []
        correspondence_records = []  # Если произошла ошибка, возвращаем пустые списки
    finally:
        # Закрываем соединение с базой данных
        if connection.is_connected():
            cursor.close()
            connection.close()

    # Передаем извлеченные данные в HTML-шаблон для отображения
    return render_template('index.html',
                           organization_records=organization_records,
                           correspondence_records=correspondence_records)

# Добавление записи в таблицу "organization_addresses"
@app.route('/organization/add', methods=['POST'])
def add_organization():
    # Получаем данные из формы
    organization_name = request.form.get('organization_name')  # Название организации
    address = request.form.get('address')  # Адрес организации
    director_lastname = request.form.get('director_lastname')  # Фамилия руководителя

    # Проверяем, что все поля заполнены
    if not organization_name or not address or not director_lastname:
        print("Ошибка: Одно или несколько полей пустые.")  # Сообщение об ошибке
        return redirect('/')  # Возврат на главную страницу

    try:
        # Подключаемся к базе данных
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # SQL-запрос для добавления новой записи в таблицу "organization_addresses"
        query = """
        INSERT INTO organization_addresses (organization_name, address, director_lastname)
        VALUES (%s, %s, %s)
        """
        # Выполняем запрос с переданными данными
        cursor.execute(query, (organization_name.strip(), address.strip(), director_lastname.strip()))
        connection.commit()  # Сохраняем изменения в базе данных

    except mysql.connector.Error as e:
        # Если произошла ошибка при добавлении записи, выводим её в консоль
        print(f"Ошибка при добавлении записи: {e}")
    finally:
        # Закрываем соединение с базой данных
        if connection.is_connected():
            cursor.close()
            connection.close()

    return redirect('/')  # Возвращаемся на главную страницу для обновления данных

# Добавление записи в таблицу "correspondence"
@app.route('/correspondence/add', methods=['POST'])
def add_correspondence():
    # Получаем данные из формы
    correspondence_type = request.form.get('correspondence_type')  # Тип корреспонденции
    preparation_date = request.form.get('preparation_date')  # Дата подготовки
    organization_name = request.form.get('organization_name')  # Название организации

    # Проверяем, что все поля заполнены
    if not correspondence_type or not preparation_date or not organization_name:
        print("Ошибка: Одно или несколько полей пустые.")  # Сообщение об ошибке
        return redirect('/')  # Возврат на главную страницу

    try:
        # Подключаемся к базе данных
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # SQL-запрос для добавления новой записи в таблицу "correspondence"
        query = """
        INSERT INTO correspondence (correspondence_type, preparation_date, organization_name)
        VALUES (%s, %s, %s)
        """
        # Выполняем запрос с переданными данными
        cursor.execute(query, (correspondence_type.strip(), preparation_date.strip(), organization_name.strip()))
        connection.commit()  # Сохраняем изменения в базе данных

    except mysql.connector.Error as e:
        # Если произошла ошибка при добавлении записи, выводим её в консоль
        print(f"Ошибка при добавлении записи: {e}")
    finally:
        # Закрываем соединение с базой данных
        if connection.is_connected():
            cursor.close()
            connection.close()

    return redirect('/')  # Возвращаемся на главную страницу для обновления данных

# Удаление записи из таблицы "organization_addresses"
@app.route('/organization/delete/<organization_name>', methods=['GET'])
def delete_organization(organization_name):
    try:
        # Подключаемся к базе данных
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # SQL-запрос для удаления записи из таблицы "organization_addresses"
        query = "DELETE FROM organization_addresses WHERE organization_name = %s"
        cursor.execute(query, (organization_name,))
        connection.commit()  # Сохраняем изменения в базе данных

    except mysql.connector.Error as e:
        # Если произошла ошибка при удалении записи, выводим её в консоль
        print(f"Ошибка при удалении записи: {e}")
    finally:
        # Закрываем соединение с базой данных
        if connection.is_connected():
            cursor.close()
            connection.close()

    return redirect('/')  # Возвращаемся на главную страницу для обновления данных

# Удаление записи из таблицы "correspondence"
@app.route('/correspondence/delete/<organization_name>', methods=['GET'])
def delete_correspondence(organization_name):
    try:
        # Подключаемся к базе данных
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # SQL-запрос для удаления записи из таблицы "correspondence"
        query = "DELETE FROM correspondence WHERE organization_name = %s"
        cursor.execute(query, (organization_name,))
        connection.commit()  # Сохраняем изменения в базе данных

    except mysql.connector.Error as e:
        # Если произошла ошибка при удалении записи, выводим её в консоль
        print(f"Ошибка при удалении записи: {e}")
    finally:
        # Закрываем соединение с базой данных
        if connection.is_connected():
            cursor.close()
            connection.close()

    return redirect('/')  # Возвращаемся на главную страницу для обновления данных

@app.route('/search', methods=['POST'])
def search():
    # Получаем поле для поиска и значение из формы
    field = request.form.get('field')  # Поле для поиска
    value = request.form.get('value')  # Значение для поиска

    # Инициализируем списки для результатов поиска и данных таблиц
    search_results = []  # Список для объединенных результатов поиска
    organization_records = []  # Данные для таблицы организаций
    correspondence_records = []  # Данные для таблицы корреспонденции

    try:
        # Подключаемся к базе данных
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Проверяем, к какой таблице относится поле, и выполняем запрос
        # Если поле из таблицы организаций
        if field in ["organization_name", "address", "director_lastname"]:
            cursor.execute(f"""
                SELECT organization_name, address, '', '', director_lastname
                FROM organization_addresses WHERE {field} = %s
            """, (value,))
            organization_results = cursor.fetchall()  # Результаты поиска в таблице организаций
        else:
            organization_results = []  # Пустой список, если поле не относится к таблице организаций

        # Если поле из таблицы корреспонденции
        if field in ["organization_name", "correspondence_type", "preparation_date"]:
            cursor.execute(f"""
                SELECT organization_name, '', correspondence_type, preparation_date, ''
                FROM correspondence WHERE {field} = %s
            """, (value,))
            correspondence_results = cursor.fetchall()  # Результаты поиска в таблице корреспонденции
        else:
            correspondence_results = []  # Пустой список, если поле не относится к таблице корреспонденции

        # Собираем все названия организаций из обеих таблиц для объединения
        organization_names = {result[0] for result in organization_results if result[0]}  # Названия из организаций
        correspondence_names = {result[0] for result in correspondence_results if result[0]}  # Названия из корреспонденции

        # Объединяем все уникальные названия организаций
        all_names = organization_names.union(correspondence_names)

        # Выполняем объединенные запросы для каждой организации
        for name in all_names:
            cursor.execute("""
                SELECT 
                    oa.organization_name,  -- Название организации
                    oa.address,            -- Адрес
                    c.correspondence_type, -- Тип корреспонденции
                    c.preparation_date,    -- Дата подготовки
                    oa.director_lastname   -- Фамилия руководителя
                FROM organization_addresses oa
                LEFT JOIN correspondence c ON oa.organization_name = c.organization_name
                WHERE oa.organization_name = %s
                UNION
                SELECT 
                    c.organization_name,  -- Название организации
                    oa.address,           -- Адрес
                    c.correspondence_type, -- Тип корреспонденции
                    c.preparation_date,    -- Дата подготовки
                    oa.director_lastname   -- Фамилия руководителя
                FROM correspondence c
                LEFT JOIN organization_addresses oa ON oa.organization_name = c.organization_name
                WHERE c.organization_name = %s
            """, (name, name))
            search_results.extend(cursor.fetchall())  # Добавляем объединенные результаты в список

        # Извлекаем все данные для таблицы организаций
        cursor.execute("SELECT organization_name, address, director_lastname FROM organization_addresses")
        organization_records = cursor.fetchall()  # Сохраняем данные для таблицы организаций

        # Извлекаем все данные для таблицы корреспонденции
        cursor.execute("SELECT correspondence_type, preparation_date, organization_name FROM correspondence")
        correspondence_records = cursor.fetchall()  # Сохраняем данные для таблицы корреспонденции

    except mysql.connector.Error as e:
        # Обрабатываем возможные ошибки подключения или выполнения запросов
        print(f"Ошибка при поиске: {e}")
    finally:
        # Закрываем соединение с базой данных
        if connection.is_connected():
            cursor.close()
            connection.close()

    # Передаем результаты поиска и данные таблиц в шаблон
    return render_template('index.html',
                           organization_records=organization_records,  # Данные для таблицы организаций
                           correspondence_records=correspondence_records,  # Данные для таблицы корреспонденции
                           search_results=search_results)  # Результаты поиска



# Запуск Flask-приложения
if __name__ == '__main__':
    # Запуск приложения в режиме отладки для отслеживания ошибок
    app.run(debug=True, host='0.0.0.0')
