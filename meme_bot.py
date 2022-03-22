from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from meme_generator import MemeGenerator

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nОтправь мне текст или картинку и я сделаю из этого мем!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Отправь мне текст или картинку и я сделаю из этого мем!")


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    photo_id = message.photo[-1].file_id
    photo = await bot.get_file(photo_id)
    file_path = photo.file_path
    await bot.download_file(file_path)
    instance = MemeGenerator.add_something(message.chat.id, image=file_path.split('/')[-1])


if __name__ == '__main__':
    executor.start_polling(dp)
