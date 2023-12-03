from aiogram import executor

from app.database import db_start
from create_bot import dp
from other.client import client
from handlers import register_callback_handlers, register_message_handlers


async def on_startup(_):
    await db_start()
    print('Bot started!')

client.start()

register_callback_handlers(dp)
register_message_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
