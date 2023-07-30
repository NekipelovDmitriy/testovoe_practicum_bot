import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import URLInputFile, FSInputFile

from config.bot_config import config
from config.utils import ABOUT_ME, GITHUB_LINK, HELP_MESSAGE


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.telegram_token.get_secret_value(), parse_mode='HTML')
dp = Dispatcher()


@dp.message(F.new_chat_members)
async def somebody_added(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f'Привет, {user.full_name}, давай познакомимся! Жми /start')


@dp.message(Command('start'))
@dp.message(lambda message: message.text == 'Главное меню')
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text='Фотки'),
            types.KeyboardButton(text='Увлечения')
        ],
        [
            types.KeyboardButton(text='Войсы'),
            types.KeyboardButton(text='GitHub')
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Давай познакомимся!"
    )
    await message.answer(ABOUT_ME, reply_markup=keyboard)


@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer(HELP_MESSAGE)


@dp.message(Command('hobbies'))
@dp.message(lambda message: message.text == 'Увлечения')
async def cmd_hobbies(message: types.Message):
    try:
        with open('media/hobbies.txt', mode="r", encoding="utf-8") as hobbies_file:
            text = hobbies_file.read()
            await message.answer(text=text, parse_mode='HTML')
    except OSError:
        await message.answer('Невозможно прочитать файл Hobbies')
        sys.exit()


@dp.message(lambda message: message.text == 'Фотки')
async def get_photo(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text='Селфи'),
            types.KeyboardButton(text='Школьное')
        ],
        [
            types.KeyboardButton(text='Главное меню')
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Давай познакомимся!"
    )
    await message.answer('Выбери, какое фото ты хочешь посмотреть', reply_markup=keyboard)


@dp.message(Command('selfie'))
@dp.message(lambda message: message.text == 'Селфи')
async def cmd_img(message: types.Message):
    image = FSInputFile("media/images/selfie.jpg")
    await message.answer_photo(
        image,
        caption="Последнее селфи"
    )


@dp.message(Command('school_photo'))
@dp.message(lambda message: message.text == 'Школьное')
async def cmd_img(message: types.Message):
    image = FSInputFile("media/images/school.jpg")
    await message.answer_photo(
        image,
        caption="Фото из школы"
    )


@dp.message(lambda message: message.text == 'Войсы')
async def get_photo(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text='Про ChatGPT'),
            types.KeyboardButton(text='Про SQL/NoSQL'),
            types.KeyboardButton(text='Про любовь')
        ],
        [
            types.KeyboardButton(text='Главное меню')
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Мои ответы на вопросы"
    )
    await message.answer('Мои ответы на вопросы', reply_markup=keyboard)


@dp.message(lambda message: message.text == 'Про ChatGPT')
async def cmd_img(message: types.Message):
    file = FSInputFile("media/audio/chatgpt.m4a")
    await message.answer_audio(
        file,
        caption="Про ЧатГПТ для бабушки"
    )

@dp.message(lambda message: message.text == 'Про SQL/NoSQL')
async def cmd_img(message: types.Message):
    file = FSInputFile("media/audio/sql.m4a")
    await message.answer_audio(
        file,
        caption="Про разницу между SQL и NoSQL"
    )

@dp.message(lambda message: message.text == 'Про любовь')
async def cmd_img(message: types.Message):
    file = FSInputFile("media/audio/love.m4a")
    await message.answer_audio(
        file,
        caption="Про первую любовь"
    )


@dp.message(Command('github'))
@dp.message(lambda message: message.text == 'GitHub')
async def cmd_github(message: types.Message):
    await message.answer(f'Репозиторий проекта: {GITHUB_LINK}')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
