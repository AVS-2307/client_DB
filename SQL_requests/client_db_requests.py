import cur as cur
import psycopg2

conn = psycopg2.connect(database="client_db", user="postgres", password="Sie555mens")

with conn.cursor() as cur:
    # удаление таблиц
    cur.execute("""
    DROP TABLE phones;
    DROP TABLE clients;
    """)

    # создание таблиц


def create_tables():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
    id SERIAL PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    surname VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL
    );  
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones(
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(40) UNIQUE,
    client_id INTEGER NOT NULL REFERENCES clients(id)
    );
    """)
    conn.commit()

    # добавление клиента


def add_client():
    cur.execute("""
           INSERT INTO clients(name, surname, email) VALUES(%s, %s, %s);
           """, ('Ivan', 'Ivanov', 'IIvanov@gmail.com'))
    conn.commit()

    # добавление телефона


def add_phone_number():
    cur.execute("""
               INSERT INTO phones(phone_number, client_id) VALUES(%s, %s);
               """, ('+79032345678', 1))
    conn.commit()

    # изменить данные о клиенте


def change_client_data():
    cur.execute("""
               UPDATE clients SET name=%s WHERE id=%s;
               """, ('Kirill', 1))
    conn.commit()

    # удалить телефон для существующего клиента


def delete_client_phone_number():
    cur.execute("""
                   DELETE FROM phones WHERE client_id=%s;
                   """, (1,))
    conn.commit()

    # удалить существующего клиента


def delete_client():
    cur.execute("""
                   DELETE FROM clients WHERE id=%s;
                   """, (1,))
    conn.commit()

    # найти клиента по его данным (имени, фамилии, email-у или телефону)


def find_client():
    cur.execute("""
                       SELECT id FROM clients WHERE surname=%s;
                       """, ('Ivanov',))
    print(cur.fetchall())


cur.close()
conn.close()
