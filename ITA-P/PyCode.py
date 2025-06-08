import sqlite3
import os

cwd = os.getcwd()
DB_pach = cwd + "\ITA-P/testDB.db"

print(f"DsDS: {DB_pach}")

def connect_db():
    conn = sqlite3.connect(DB_pach)
    return conn

def create_table(): # Добавление всех таблиц. Выпольняется один раз, после создания базы данных, последущая активация вызывет ошибку
    conn = sqlite3.connect()
    cur = conn.cursor()

    create_t_user_data = """
        Create table User_data (
            User_id INTEGER PRIMARY KEY ,
            Telegram_user_id NULL,
            FIO VARCHAR(255) NOT NULL ,
            Date_brith Date not null,
            Gender VARCHAR(10) NOT NULL CHECK(Gender IN ('М', 'Ж')),
            Year_grad_fr_school INT NOT NULL CHECK(Year_grad_fr_school > 1900)
        );
        """
    
    create_t_user_rights = """
        Create table User_rights(
            User_id INT NOT NULL ,
            User_type VARCHAR(10) NOT NULL CHECK(User_type IN ('Admin', 'admin', 'A', 'a', 'User', 'user', 'U', 'u', 'Test', 'test', 'T', 't')) ,
            -- 
            constraint pk_user_id_rights foreign key (User_id) 
            references User_data(User_id)
        );
    """
    
    create_t_users_contacts = """
        Create table Users_contacts(
            User_id INT NOT NULL ,
            Email VARCHAR(255) NULL ,
            Phone VARCHAR(20) NULL ,

            constraint pk_user_id_contacts foreign key (User_id)
            references User_data(User_id)
        );
    """

    create_t_faculty = """
        CREATE TABLE Faculty(
            Faculty_id INTEGER PRIMARY KEY,
            Faculty_name VARCHAR(255) NOT NULL
        );
    """

    t_user_fraculty = """
        CREATE TABLE User_faculty(
            User_id INT NOT NULL ,
            Faculty_id INT NOT NULL,

            constraint pk_user_id_faculty foreign key (User_id) 
            references User_data(User_id),
            --

            constraint pk_faculty foreign key (Faculty_id) 
            references Faculty(Faculty_id)
        );
    """
    
    try:
        cur.execute(create_t_user_data)
        cur.execute(create_t_user_rights)
        cur.execute(create_t_users_contacts)
        cur.execute(create_t_faculty)
        cur.execute(t_user_fraculty)
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблиц: {e}")
    finally:
        conn.commit()
        conn.close()

def insert_facultet(): # Добавление факультетов
    conn = connect_db()
    cursor = conn.cursor()


    insert_fac = """
        INSERT INTO Faculty(Faculty_name) VALUES 
        ('Факультет информационных технологий и управления'),
        ('Факультет филологии'),
        ('Факультет биологии'),
        ('Факультет права и социальных технологий'),
        ('Факультет естественных наук и технологий'),
        ('Экономический факультет');
    """
    try:
        cursor.execute(insert_fac)
    except sqlite3.Error as e:
        print(f"Ошибка при вставке данных в таблицу: {e}")
    finally:
        conn.commit()
        conn.close()

def insert_sample_data(user_id): #Добавление тестового пользователя
    conn = connect_db()
    cursor = conn.cursor()

    insert_user = """
        INSERT INTO User_data(User_id, FIO, Date_brith, Gender, Year_grad_fr_school) VALUES (?, ?, ?, ?, ?);
    """
    insert_rights = """
        Insert INTO User_rights(User_id, User_type) VALUES (?, ?);
    """
    insert_user_contacts = """
        Insert into Users_contacts(User_id, Email, Phone) VALUES (?, ?, ?);
    """

    user_data = (user_id, 'Иван Иванов Иванович', "1999-01-01", 'М', 2019)
    user_rights = (user_id, 'Test')
    user_contacts = (user_id, 'ivanivanov@gmail.com', '+7(888)999-01-01')

    try:
        cursor.execute(insert_user, user_data)
        cursor.execute(insert_rights, user_rights)
        cursor.execute(insert_user_contacts, user_contacts)
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении тестового пользователя данных в таблицу: {e}")
    finally:
        conn.commit()
        conn.close()

def insert_user_data(User_type, FIO, Date_brith, Gender, Year_grad_fr_school, Email, Phone): # Функция для добавления пользователя в базу данных
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM User_data;")
    row_count = cursor.fetchone()[0]
    user_id = row_count + 1

    Phone = Phone+""
    if len(Phone) < 11: 
        return -1
        

    insert_user = """
        INSERT INTO User_data(User_id, FIO, Date_brith, Gender, Year_grad_fr_school) VALUES (?, ?, ?, ?, ?);
    """
    insert_rights = """
        Insert INTO User_rights(User_id, User_type) VALUES (?, ?);
    """
    insert_user_contacts = """
        Insert into Users_contacts(User_id, Email, Phone) VALUES (?, ?, ?);
    """
    user_data = (user_id, FIO, Date_brith, Gender, Year_grad_fr_school)
    user_rights = (user_id, User_type)
    user_contacts = (user_id, Email, Phone)

    try:
        cursor.execute(insert_user, user_data)
        cursor.execute(insert_rights, user_rights)
        cursor.execute(insert_user_contacts, user_contacts)
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении тестового пользователя данных в таблицу: {e}")
    finally:
        conn.commit()
        conn.close()

def find_user(name_fio): # поиск пользователя по ФИО. Возвращает список id пользователей найденных по паттерну, если нечего не найденно возвращает -1
    conn = connect_db()
    cursor = conn.cursor()

    pattern = f"{name_fio}%"

    query = "SELECT User_id FROM User_data WHERE FIO LIKE ?"
    cursor.execute(query, (pattern,))
    result = cursor.fetchall()
    conn.close()

    if result:
        ex = []
        for i in result:
            ex.append(i[0])
        return ex
    else:
        return -1


if __name__ == '__main__':
    print("Heloo E.T.A")
    fio = find_user("Иванов Иван")
    print(fio)
    print("Good E.T.A")




