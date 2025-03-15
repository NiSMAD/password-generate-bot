import asyncio
import random
import string
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.command import Command

TELEGRAM_TOKEN = ""

bot = Bot(token=TELEGRAM_TOKEN)

dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Это бот, который генерирует пароль из введеных тобой параметров.")
    await button_message(message)

async def button_message(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
                [KeyboardButton(text="Лёгкий пароль")],
                [KeyboardButton(text="Средний пароль")],
                [KeyboardButton(text="Сложный пароль")]
            ],
        resize_keyboard=True,
    )
    await message.answer("""Если вы хотите сгенерировать пароль, нажмите на одну из кнопок ниже.

Узнать о подробностях градации паролей можно написав компанду: /info""", reply_markup=keyboard)

@dp.message(Command("info"))
async def info_command(message: Message):
    await message.answer("""<b>Виды паролей</b>:
 ~ ~ ~ 
<b>Лёгкий пароль</b>: Короткий пароль без специальных символов и разных регистров
 - - -
<b>Средний пароль</b>: Используются заглавные и строчные буквы, цифры, спецсимволы.
 - - -
<b>Сложный пароль</b>: Случайные символы, минимум 12-16 знаков, использование всех типов символов.
 ~ ~ ~
""", parse_mode="html")

@dp.message(lambda message: message.text in "Лёгкий пароль")
async def easy_password(message: Message):
    password = ""
    for _ in range(random.randint(5, 6)):
        password += chr(ord('a') + random.randint(0, 25))
    await message.answer(f"Сгенерированный пароль: {password}")

@dp.message(lambda message: message.text in "Средний пароль")
async def medium_password(message: Message):
    password = ""
    for _ in range(random.randint(7, 8)):
        password += chr(ord('a') + random.randint(0, 25))
        password += chr(ord('A') + random.randint(0, 25))
        password += str(random.randint(0, 9))
    password += random.choice("!@#$%^&*()_+=-{}[];':\",.<>/?")
    await message.answer(f"Сгенерированный пароль: {password}")

@dp.message(lambda message: message.text in "Сложный пароль")
async def hard_password(message: Message):
    password = ""
    for _ in range(random.randint(10, 12)):
        password += chr(ord('a') + random.randint(0, 25))
        password += chr(ord('A') + random.randint(0, 25))
        password += str(random.randint(0, 9))
    password += random.choice("!@#$%^&*()_+=-{}[];':\",.<>/?")
    for _ in range(random.randint(0, 5)):
        password += random.choice(string.ascii_letters + string.digits + "!@#$%^&*()_+=-{}[]|;':\",.<>/?")
    await message.answer(f"Сгенерированный пароль: {password}")


@dp.message(Command("generate_password"))
async def generate_password_command(message: Message, password_length: int, uppercase_letters: int, lowercase_letters: int, digits: int, special_characters: int):
    password = ""
    for _ in range(password_length):
        if uppercase_letters > 0:
            password += chr(ord('A') + random.randint(0, 25))
            uppercase_letters -= 1
        if lowercase_letters > 0:
            password += chr(ord('a') + random.randint(0, 25))
            lowercase_letters -= 1
        if digits > 0:
            password += str(random.randint(0, 9))
            digits -= 1
        if special_characters > 0:
            password += random.choice("!@#$%^&*()_+=-{}[]|;':\",.<>/?")
            special_characters -= 1
    await message.answer(f"Сгенерированный пароль: {password}")



if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
