import psycopg2
import csv

# Функция для подключения к базе данных
def connect_db():
    return psycopg2.connect(
        host="localhost",
        dbname="phonebook_db",
        user="postgres",
        password="Karim2005"  
    )

# Создание таблицы PhoneBook
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS PhoneBook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            phone_number VARCHAR(20)
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()


def create_functions_and_procedures():
    conn = connect_db()
    cur = conn.cursor()

    
    cur.execute('''
    CREATE OR REPLACE FUNCTION get_records_by_pattern(p_pattern VARCHAR)
    RETURNS SETOF PhoneBook AS $$
    BEGIN
        RETURN QUERY
        SELECT * FROM PhoneBook
        WHERE first_name ILIKE '%' || p_pattern || '%'
           OR phone_number ILIKE '%' || p_pattern || '%';
    END;
    $$ LANGUAGE plpgsql;
    ''')

    # Процедура для вставки/обновления пользователя
    cur.execute('''
    CREATE OR REPLACE PROCEDURE upsert_user(p_name VARCHAR, p_phone VARCHAR)
    LANGUAGE plpgsql
    AS $$
    DECLARE
        user_count INT;
    BEGIN
        SELECT COUNT(*) INTO user_count FROM PhoneBook WHERE first_name = p_name;
        IF user_count > 0 THEN
            UPDATE PhoneBook SET phone_number = p_phone WHERE first_name = p_name;
        ELSE
            INSERT INTO PhoneBook(first_name, phone_number) VALUES (p_name, p_phone);
        END IF;
    END;
    $$;
    ''')

    cur.execute('''
    CREATE OR REPLACE PROCEDURE insert_many_users(p_names VARCHAR[], p_phones VARCHAR[])
    LANGUAGE plpgsql
    AS $$
    DECLARE
        i INT;
        invalid_data RECORD;
    BEGIN
        IF array_length(p_names, 1) != array_length(p_phones, 1) THEN
            RAISE EXCEPTION 'Длина массивов имен и телефонов не совпадает';
        END IF;

        CREATE TEMP TABLE invalid_users (name VARCHAR, phone VARCHAR);

        FOR i IN 1..array_length(p_names, 1) LOOP
            IF p_phones[i] ~ '^[0-9]+$' AND length(p_phones[i]) >= 5 THEN
                CALL upsert_user(p_names[i], p_phones[i]);
            ELSE
                INSERT INTO invalid_users VALUES (p_names[i], p_phones[i]);
            END IF;
        END LOOP;

        -- Выведем некорректные данные
        RAISE NOTICE 'Некорректные данные:';
        FOR invalid_data IN SELECT * FROM invalid_users LOOP
            RAISE NOTICE 'Name: %, Phone: %', invalid_data.name, invalid_data.phone;
        END LOOP;
    END;
    $$;
    ''')

    
    cur.execute('''
    CREATE OR REPLACE FUNCTION get_records_with_pagination(p_limit INT, p_offset INT)
    RETURNS SETOF PhoneBook AS $$
    BEGIN
        RETURN QUERY
        SELECT * FROM PhoneBook
        ORDER BY id
        LIMIT p_limit OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;
    ''')

    # Процедура для удаления данных
    cur.execute('''
    CREATE OR REPLACE PROCEDURE delete_records(p_name VARCHAR, p_phone VARCHAR)
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF p_name IS NOT NULL THEN
            DELETE FROM PhoneBook WHERE first_name = p_name;
        ELSIF p_phone IS NOT NULL THEN
            DELETE FROM PhoneBook WHERE phone_number = p_phone;
        ELSE
            RAISE NOTICE 'Ничего не удалено, не указаны параметры.';
        END IF;
    END;
    $$;
    ''')

    conn.commit()
    cur.close()
    conn.close()

# Вставка данных из CSV файла
def insert_from_csv():
    filename = input("Введите имя CSV файла: ")
    try:
        conn = connect_db()
        cur = conn.cursor()
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  
            for row in reader:
                cur.execute("INSERT INTO PhoneBook (first_name, phone_number) VALUES (%s, %s)", (row[0], row[1]))
        conn.commit()
        print("Данные из CSV файла добавлены.")
    except FileNotFoundError:
        print("CSV файл не найден.")
    finally:
        cur.close()
        conn.close()

# Вставка данных с консоли
def insert_from_console():
    first_name = input("Введите имя: ")
    phone_number = input("Введите номер телефона: ")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO PhoneBook (first_name, phone_number) VALUES (%s, %s)", (first_name, phone_number))
    conn.commit()
    cur.close()
    conn.close()
    print("Данные добавлены.")

# Обновление данных
def update_data():
    conn = connect_db()
    cur = conn.cursor()
    old_name = input("Введите имя пользователя для обновления: ")
    new_name = input("Введите новое имя (оставьте пустым, если не нужно менять): ")
    new_phone = input("Введите новый номер телефона (оставьте пустым, если не нужно менять): ")

    if new_name:
        cur.execute("UPDATE PhoneBook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
    if new_phone:
        cur.execute("UPDATE PhoneBook SET phone_number = %s WHERE first_name = %s", (new_phone, new_name or old_name))
    conn.commit()
    cur.close()
    conn.close()
    print("Данные обновлены.")

# Запрос данных с фильтрами
def query_data():
    conn = connect_db()
    cur = conn.cursor()
    print("1. Поиск по имени")
    print("2. Поиск по номеру телефона")
    print("3. Показать все записи")
    choice = input("Выберите фильтр: ")

    if choice == '1':
        filter_name = input("Введите имя для поиска: ")
        cur.execute("SELECT * FROM PhoneBook WHERE first_name = %s", (filter_name,))
    elif choice == '2':
        filter_phone = input("Введите номер телефона для поиска: ")
        cur.execute("SELECT * FROM PhoneBook WHERE phone_number = %s", (filter_phone,))
    elif choice == '3':
        cur.execute("SELECT * FROM PhoneBook")
    else:
        print("Неверный выбор.")
        cur.close()
        conn.close()
        return

    rows = cur.fetchall()
    for row in rows:
        print(f"id: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
    cur.close()
    conn.close()

# Удаление данных
def delete_data():
    conn = connect_db()
    cur = conn.cursor()
    print("1. Удалить по имени")
    print("2. Удалить по номеру телефона")
    choice = input("Выберите метод удаления: ")

    if choice == '1':
        del_name = input("Введите имя для удаления: ")
        cur.execute("DELETE FROM PhoneBook WHERE first_name = %s", (del_name,))
    elif choice == '2':
        del_phone = input("Введите номер телефона для удаления: ")
        cur.execute("DELETE FROM PhoneBook WHERE phone_number = %s", (del_phone,))
    else:
        print("Неверный выбор.")
        cur.close()
        conn.close()
        return
    conn.commit()
    cur.close()
    conn.close()
    print("Данные удалены.")


# Поиск по шаблону с использованием созданной функции
def search_by_pattern():
    pattern = input("Введите шаблон для поиска (часть имени или телефона): ")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_records_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f"id: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
    else:
        print("Нет записей по данному шаблону.")
    cur.close()
    conn.close()

# Вставка или обновление пользователя (upsert)
def upsert_user_data():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("CALL upsert_user(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Операция выполнена (вставка или обновление).")

# Массовая вставка пользователей
def insert_many_users_data():
    
    n = int(input("Сколько записей вы хотите вставить? "))
    names = []
    phones = []
    for i in range(n):
        print(f"Запись #{i+1}:")
        nm = input("Имя: ")
        ph = input("Телефон: ")
        names.append(nm)
        phones.append(ph)

    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
    conn.commit()
    cur.close()
    conn.close()
    print("Массовая вставка выполнена. Проверьте серверные сообщения на некорректные данные.")


def pagination_query():
    limit = int(input("Введите лимит: "))
    offset = int(input("Введите смещение (offset): "))
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_records_with_pagination(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f"id: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
    else:
        print("Нет записей на данной странице.")
    cur.close()
    conn.close()

# Удаление 
def delete_records_procedure():
    choice = input("Удалить по (1) имени или (2) номеру телефона: ")
    conn = connect_db()
    cur = conn.cursor()
    if choice == '1':
        name_to_delete = input("Введите имя: ")
        cur.execute("CALL delete_records(%s, NULL)", (name_to_delete,))
    elif choice == '2':
        phone_to_delete = input("Введите телефон: ")
        cur.execute("CALL delete_records(NULL, %s)", (phone_to_delete,))
    else:
        print("Неверный выбор.")
        cur.close()
        conn.close()
        return
    conn.commit()
    cur.close()
    conn.close()
    print("Данные удалены (или не были найдены).")


# Главное меню
def main():
    create_table()
    create_functions_and_procedures()

    while True:
        print("\nВыберите действие:")
        print("1. Вставить данные из CSV файла")
        print("2. Вставить данные с консоли")
        print("3. Обновить данные")
        print("4. Запросить данные")
        print("5. Удалить данные")
        print("6. Поиск по шаблону (Функция из lab11")
        print("7. Upsert (добавить или обновить) пользователя lab11")
        print("8. Массовая вставка с проверкой телефонов lab11")
        print("9. Навигация lab11)")
        print("10. Удаление через процедуру lab11")
        print("11. Выход")
        choice = input("Введите номер действия: ")

        if choice == '1':
            insert_from_csv()
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_data()
        elif choice == '4':
            query_data()
        elif choice == '5':
            delete_data()
        elif choice == '6':
            search_by_pattern()
        elif choice == '7':
            upsert_user_data()
        elif choice == '8':
            insert_many_users_data()
        elif choice == '9':
            pagination_query()
        elif choice == '10':
            delete_records_procedure()
        elif choice == '11':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()
