import psycopg2

dbname = "UNN_poll"
user = "postgres"
password = "vjz,fpflfyys[23"
host = "localhost"
port = "5432"

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

cur = conn.cursor()

async def set_col(user_id, name, age, phone_number):
    cur.execute("INSERT INTO users (user_id, name, age, phone_number) VALUES (%s, %s, %s, %s)", (user_id, name, age, phone_number))
    conn.commit()

async def search_user_id(userid):
    cur.execute("SELECT user_id FROM users WHERE user_id = %s", (userid,))
    uid = cur.fetchone()
    if uid is not None:
        return uid[0]
    else:
        return False

async def show_id(userid):
    cur.execute("SELECT name, age, phone_number FROM users WHERE user_id = %s", (userid,))
    user_info = cur.fetchone()
    if user_info is not None:
        return user_info
    else:
        return False

async def update_user_info(user_id, name=None, age=None, phone_number=None):
    if name:
        cur.execute("UPDATE users SET name = %s WHERE user_id = %s", (name, user_id))
    if age:
        cur.execute("UPDATE users SET age = %s WHERE user_id = %s", (age, user_id))
    if phone_number:
        cur.execute("UPDATE users SET phone_number = %s WHERE user_id = %s", (phone_number, user_id))
    conn.commit()
