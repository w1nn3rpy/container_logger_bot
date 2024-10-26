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
        await message.reply('Начинаю отправлять логи в реальном времени\n')
        async for log in stream_logs():
            await bot.send_message(chat_id=int(config('CHAT_ID')), text=log)
            await asyncio.sleep(1)
    else:
        await message.reply('Ты левый чел')

@dp.message(Command('restart'))
async def restart_container(message: Message):
    await message.reply('Перезапускаю контейнер')
    container = client.containers.get(container_name)
    container.restart()
    await asyncio.sleep(10)
    container.reload()
    if container.status == 'running':
        await message.reply('Контейнер запущен')
    else:
        await message.reply('Контейнер не запустился')



async def stream_logs():
    loop = asyncio.get_event_loop()
    generator = stream_container_logs()
    while True:
        log = await asyncio.to_thread(next, generator, None)
        if log is None:
            break
        yield log



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
