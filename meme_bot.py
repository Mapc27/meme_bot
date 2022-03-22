from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from meme_generator import MemeGenerator
from aiogram.types import input_file

import aiohttp

from config import TOKEN, IMAGES_FOLDER_NAME

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
    await bot.download_file(file_path, destination_dir="./")
    instance = MemeGenerator.add_something(message.chat.id, image=file_path.split('/')[-1])
    await if_instance_ready(instance)


@dp.message_handler(content_types=['text'])
async def handle_text(message):
    if message.text.startswith('http://') or message.text.startswith('https://'):
        async with aiohttp.ClientSession() as session:
            url = message.text
            print(url)
            async with session.get(url) as resp:
                print(resp)
                if resp.status == 200:
                    with open(f'{IMAGES_FOLDER_NAME}/{url.split("/")[-1]}', mode='wb') as f:
                        f.write(await resp.read())
                        f.close()
                instance = MemeGenerator.add_something(message.chat.id, image=url.split("/")[-1])
                await if_instance_ready(instance)
    else:
        instance = MemeGenerator.add_something(message.chat.id, caption=message.text)
        await if_instance_ready(instance)


async def send_meme(authors: [], file_name: str):
    for author in authors:
        photo = input_file.InputFile(f'{IMAGES_FOLDER_NAME}/{file_name}')
        await bot.send_photo(chat_id=author, photo=photo)


async def if_instance_ready(instance):
    if instance.ready():
        file_name = instance.generate()
        await send_meme(instance.authors, file_name)
        instance.delete()
        del instance


if __name__ == '__main__':
    executor.start_polling(dp)
