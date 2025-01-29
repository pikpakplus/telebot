from aiogram import Router, types
from aiogram.filters import Command
from bot_config import database

show_books_router = Router()


@show_books_router.message(Command('showbooks'))
async def show_books(message: types.Message):
    books = database.get_books()

    if not books:
        await message.answer("База данных книг пуста.")
        return

    text = "*Список книг:*\n\n"
    for book in books:
        text += f"*{book[1]}*\nГод: {book[2]}\nАвтор: {book[3]}\nЖанр: {book[4]}\nЦена: {book[5]} ₽\n\n"

    await message.answer(text, parse_mode="Markdown")
