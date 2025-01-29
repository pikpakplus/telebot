from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database import Database

book_admin_router = Router()

db = Database()


class Books(StatesGroup):
    name = State()
    year = State()
    author = State()
    genre = State()
    price = State()


@book_admin_router.message(Command('newbook'))
async def new_book(message: types.Message, state: FSMContext):
    await message.answer('Введите название книги')
    await state.set_state(Books.name)


@book_admin_router.message(Books.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите год издания книги')
    await state.set_state(Books.year)


@book_admin_router.message(Books.year)
async def process_author(message: types.Message, state: FSMContext):
    year = message.text
    if not year.isdigit():
        await message.answer("Вводите только цифры")
        return
    year = int(year)
    if year < 0 or year > 2025:
        await message.answer('Вводите только точную дату')
        return
    await state.update_data(year=message.text)
    await message.answer('Введите автора книги')
    await state.set_state(Books.author)


@book_admin_router.message(Books.author)
async def process_genre(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await message.answer('Введите жанр книги')
    await state.set_state(Books.genre)


@book_admin_router.message(Books.genre)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await message.answer('Введите стоимость книги')
    await state.set_state(Books.price)


@book_admin_router.message(Books.price)
async def process_finish(message: types.Message, state: FSMContext):
    price = message.text
    if not price.isdigit():
        await message.answer("Вводите только цифры")
        return
    price = int(price)
    if price <= 0:
        await message.answer('Вводите только положительную цену')
        return
    await state.update_data(price=message.text)
    data = await state.get_data()
    db.save_book(
        data.get('name'),
        data.get('year'),
        data.get('author'),
        data.get('genre'),
        data.get('price')
    )
    await message.answer('Спасибо, книга была сохранена')
    await state.clear()
