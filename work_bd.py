import psycopg2
import configparser


# Функция для чтения password (пароль к postgresSQL),
# name_bd (название базы данных) из файла 'password.ini'
def get_password():
    data = configparser.ConfigParser()
    data.read('password.ini')
    password = data["password"]["password"]
    name_bd = data["password"]["name_bd"]
    return [password, name_bd]

# Функция DROP удаления (если есть) и создания (без данных) таблиц VK_Partners, VK_Photos, VK_Settings
def create_table():
    with psycopg2.connect(database=get_password()[1], user="postgres", password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DROP TABLE IF EXISTS VK_Partners;
                DROP TABLE IF EXISTS VK_Photos;
                DROP TABLE IF EXISTS VK_Settings;
                """)
            conn.commit()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS VK_Partners (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100),
                    partner_id VARCHAR(20) NOT NULL,
                    favorite BOOLEAN NOT NULL DEFAULT False,
                    ban BOOLEAN NOT NULL DEFAULT False);
                 """)
            conn.commit()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS VK_Photos (
                    id SERIAL PRIMARY KEY,
                    partner_id VARCHAR(20) NOT NULL,
                    photo_link VARCHAR(100) NOT NULL);
                """)
            conn.commit()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS VK_Settings (
                    id SERIAL PRIMARY KEY,
                    conf_name VARCHAR(20) NOT NULL,
                    conf_value VARCHAR(100) NOT NULL);
                 """)
            conn.commit()


# Функция добавления партнеров в таблицу VK_Partners
def add_VK_Partners(first_name, last_name, partner_id):
    with psycopg2.connect(database=get_password()[1], user="postgres", password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO VK_Partners(first_name, last_name, partner_id) 
                VALUES(%s, %s, %s)
                RETURNING first_name, last_name, partner_id, favorite, ban
                """, (first_name, last_name, partner_id))
            new_VK_Partners = cur.fetchone()
            print(f'Добавлен партнер {new_VK_Partners}')
            conn.commit()
    conn.close()


# Функция добавления фото в таблицу VK_Partners
def add_VK_Photos(partner_id, photo_link):
    with psycopg2.connect(database=get_password()[1], user="postgres", password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO VK_Photos(partner_id, photo_link) 
                VALUES(%s, %s)
                RETURNING partner_id, photo_link
                """, (partner_id, photo_link))
            new_VK_Photos = cur.fetchone()
            print(f'Добавлено фото партнера id({new_VK_Photos[0]}) link({new_VK_Photos[1]})')
            conn.commit()
    conn.close()

# Функция получения количества партнеров
def select_count_partners():
    with psycopg2.connect(database=get_password()[1], user="postgres", password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*)
                FROM VK_Partners
                """)
            count = cur.fetchone()
            return count
            conn.commit()
    conn.close()


# Функция проверки, что партнер (partner_id) в бане (ban = True или False)
def check_ban_partner(partner_id):
    with psycopg2.connect(database=get_password()[1], user="postgres", password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT ban
                FROM VK_Partners
                WHERE partner_id = %s;
                """, (partner_id,))
            check_ban = cur.fetchone()
            return check_ban
            conn.commit()
    conn.close()

# Функция добавления партнера (partner_id) в бан (ban = True)
def add_ban_partner(partner_id):
    with psycopg2.connect(database=get_password()[1], user="postgres", password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE VK_Partners
                SET ban = True
                WHERE partner_id = %s;
                """, (partner_id,))
            conn.commit()
    conn.close()

# Функция проверки, что партнер (partner_id) в избранном (favorite = True или False)
def check_favorite_partner(partner_id):
    with psycopg2.connect(database=get_password()[1], user="postgres", password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT favorite
                FROM VK_Partners
                WHERE partner_id = %s;
                """, (partner_id,))
            check_favorite = cur.fetchone()
            return check_favorite
            conn.commit()
    conn.close()

# Функция добавления партнера (partner_id) в избранное (favorite = True)
def add_favorite_partner(partner_id):
    with psycopg2.connect(database=get_password()[1], user="postgres", password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE VK_Partners
                SET favorite = True
                WHERE partner_id = %s;
                """, (partner_id,))
            conn.commit()
    conn.close()


# Функция получения всех данных о партнере (имя, фамилия, id, фото)
def select_partner(partner_id):
    with psycopg2.connect(database=get_password()[1], user="postgres", password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT first_name, last_name, VK_Partners.partner_id, photo_link
                FROM VK_Partners JOIN VK_Photos ON VK_Partners.partner_id = VK_Photos.partner_id
                WHERE VK_Partners.partner_id = %s;
                """, (partner_id,))
            partner = cur.fetchall()
            return partner
            conn.commit()
    conn.close()


# Функция получаем фото из таблицы VK_Photos по partner_id (id партнера)
def get_photo(partner_id):
    with psycopg2.connect(database=get_password()[1], user="postgres", password=get_password()[0]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT photo_link
                FROM VK_Photos
                WHERE partner_id = %s;
                """, (partner_id,))
            photo = cur.fetchall()
            return photo
            conn.commit()
    conn.close()