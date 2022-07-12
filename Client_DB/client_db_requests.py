import psycopg2

conn = psycopg2.connect(database="client_db", user="postgres", password="Sie555mens")

with conn.cursor() as cur:
    # удаление таблиц

    def delete_tables():
        cur.execute("""
        DROP TABLE clients, phones CASCADE;
        """)


    delete_tables()

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


    create_tables()

    # добавление клиента

    def add_client():
        name = input('Введите имя нового клиента: ')
        surname = input('Введите фамилию нового клиента: ')
        email = input('Введите email нового клиента: ')
        cur.execute("""
               INSERT INTO clients(name, surname, email) VALUES(%s, %s, %s) Returning Id;
               """, (name, surname, email))
        print(f'Порядковый номер нового клиента: {cur.fetchall()}\n'
              f'Клиент {name} {surname} успешно добавлен')


    add_client()

    # добавление телефона

    def add_phone_number():
        phone_number = int(input('Введите телефонный номер клиента: '))
        client_id = input('Введите id клиента: ')
        cur.execute("""
                   INSERT INTO phones(phone_number, client_id) VALUES(%s, %s) Returning id;
                   """, (phone_number, client_id))
        print(f'Номер {phone_number} для клиента с Client_id {cur.fetchall()} успешно добавлен')


    add_phone_number()

    # изменить данные о клиенте

    def change_client_data():
        req = int(input('Что необходимо изменить, выберите вариант:\n'
                        '1. Имя клиента\n'
                        '2. Фамилия клиента\n'
                        '3. Email клиента\n'
                        '4. Телефонный номер клиента\n'))
        if req == 1:
            name = (input('Введите имя клиента для изменения:'))
            client_id = int(input('Введите id клиента, имя которого нужно изменить:'))
            cur.execute("""
                        UPDATE clients SET name=%s WHERE id=%s Returning id;
                        """, (name, client_id))
            print(f'Имя {name} для клиента с Client_id {cur.fetchall()} успешно изменено')
        if req == 2:
            surname = (input('Введите фамилию клиента для изменения:'))
            client_id = int(input('Введите id клиента, фамилию которого нужно изменить:'))
            cur.execute("""
                        UPDATE clients SET surname=%s WHERE id=%s Returning id;
                        """, (surname, client_id))
            print(f'Фамилия {surname} для клиента с Client_id {cur.fetchall()} успешно изменена')
        if req == 3:
            email = (input('Введите email клиента для изменения:'))
            client_id = int(input('Введите id клиента, email которого нужно изменить:'))
            cur.execute("""
                        UPDATE clients SET email=%s WHERE id=%s Returning id;
                        """, (email, client_id))
            print(f'Email {email} для клиента с Client_id {cur.fetchall()} успешно изменен')
        if req == 4:
            phone_number = int(input('Введите телефонный номер клиента для изменения:'))
            client_id = int(input('Введите id клиента, телефонный номер которого нужно изменить:'))
            cur.execute("""
                        UPDATE phones SET phone_number=%s WHERE id=%s Returning id;
                        """, (phone_number, client_id))
            print(f'Телефонный номер {phone_number} для клиента с Client_id {cur.fetchall()} успешно изменен')


    change_client_data()

    # удалить телефон для существующего клиента

    def delete_client_phone_number():
        phone_number = int(input('Введите номер телефона клиента для удаления:'))
        client_id = int(input('Введите id клиента, телефонный номер которого нужно удалить:'))
        cur.execute("""
                   DELETE FROM phones WHERE id=%s Returning id;
                   """, (phone_number,))
        conn.commit()
        print(f'Телефонный номер {phone_number} для клиента с Client_id {client_id} успешно удален')


    delete_client_phone_number()

    # удалить существующего клиента

    def delete_client():
        name = input('Введите имя клиента для удаления:')
        surname = input('Введите фамилию клиента:')
        client_id = int(input('Введите id клиента:'))
        cur.execute("""
                            DELETE FROM phones WHERE id=%s ;
                            """, (client_id,))
        cur.execute("""
                    DELETE FROM clients WHERE id=%s ;
                    """, (client_id,))

        conn.commit()
        print(f'Клиент {name} {surname} с номером {client_id} успешно удален')


    delete_client()

    # найти клиента по его данным (имени, фамилии, email-у или телефону)

    def find_client():
        req = input('Поиск по каким параметрам Вам требуется?\n'
                    'Введите порядковый номер согласно списку ниже:\n'
                    '1. Поиск по фамилии\n'
                    '2. Поиск по имени\n'
                    '3. Поиск по email\n'
                    '4. Поиск по номеру телефона\n')
        if req == 1:
            surname = input('Введите фаимилию клиента для поиска:')
            cur.execute("""
                       SELECT id FROM clients WHERE surname=%s;
                       """, (surname,))
        print(cur.fetchall())
        if req == 2:
            name = input('Введите имя клиента для поиска:')
            cur.execute("""
                       SELECT id FROM clients WHERE name=%s;
                       """, (name,))
        print(cur.fetchall())
        if req == 3:
            email = input('Введите email клиента для поиска:')
            cur.execute("""
                                   SELECT id FROM clients WHERE email=%s;
                                   """, (email,))
        print(cur.fetchall())
        if req == 4:
            phone_number = int(input('Введите номер телефона клиента для поиска:'))
            cur.execute("""
                                   SELECT id FROM clients WHERE phone_number=%s;
                                   """, (phone_number,))
        print(cur.fetchall())

# if __name__ == '__main__':
#     Choice = int(input('Выберите вариант взаимодействия с БД:\n'
#                        '1. Создание таблиц БД\n'
#                        '2. Добавление клиента\n'
#                        '3. Добавление телефонного номера клиента\n'
#                        '4. Изменение данные клиента\n'
#                        '5. Удаление телефонного номера клиента\n'
#                        '6. Удаление клиента\n'
#                        '7. Поиск клиента\n'
#                        ''))
#     if Choice == 1:
#         create_tables()
#     elif Choice == 2:
#         add_client()
#     elif Choice == 3:
#         add_phone_number()
#     elif Choice == 4:
#         change_client_data()
#     elif Choice == 5:
#         delete_client_phone_number()
#     elif Choice == 6:
#         delete_client()
#     elif Choice == 7:
#         find_client()
#     else:
#         print('Введен неверный вариант')
#
conn.close()
