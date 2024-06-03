import asyncio
from aiogram import Bot, Dispatcher
from database import conn
from handlers import router
import psycopg2


dbname = "UNN_poll"
user = "postgres"
password = "vjz,fpflfyys[23"
host = "localhost"
port = "5432"

async def if_con():
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    if conn:
        print("соединение установлено")
    else:
        print("что-то с базой")

async def main():
    await if_con()
    bot = Bot(token ="6458503910:AAGORHNT4np02C_8kp8EaYyTBrdiLxmUnVs")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('выключен')