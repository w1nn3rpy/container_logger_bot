from decouple import config
import asyncio
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import logging
from docker_logging import *
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)


bot = Bot(token=config('BOT_TOKEN'))
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command('start'))
async def start_handler(message: Message):
    await message.reply('А ты чё пришёл сюда? Этот бот не для тебя)))')


@dp.message(Command('logs'))
async def send_logs(message: Message):
    if message.from_user.id == int(config('CHAT_ID')):
        logs = get_container_logs()
        if logs:
            await message.reply(logs)
        else:
            await message.reply('Логов нет')
    else:
        await message.reply('Ты левый чел')


# Периодическая отправка логов
async def periodic_log_sender():
    while True:
        try:
            logs = get_container_logs()
            if logs:
                await bot.send_message(chat_id=int(config('CHAT_ID')), text=f'Логи:\n {logs}')
            await asyncio.sleep(60)  # Интервал в секундах
        except Exception as e:
            return f'Ошибка при периодической отправке логов: {e}'


async def main():
    asyncio.create_task(periodic_log_sender())
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
