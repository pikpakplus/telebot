from aiogram import Router, types
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
from database import Database


review_router = Router()
db = Database()


class BooksReview(StatesGroup):
    waiting_for_name = State()
    waiting_for_contact = State()
    waiting_for_date = State()
    waiting_for_rate = State()
    waiting_for_extra_comments = State()


@review_router.callback_query(lambda call: call.data == "review:start")
async def start_review(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Как вас зовут?")
    await state.set_state(BooksReview.waiting_for_name)
    await callback.answer()


@review_router.message(BooksReview.waiting_for_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш номер телефона или инстаграм:")
    await state.set_state(BooksReview.waiting_for_contact)


@review_router.message(BooksReview.waiting_for_contact)
async def get_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer("Введите дату посещения в формате ГГГГ-ММ-ДД (или напишите 'пропустить'):")
    await state.set_state(BooksReview.waiting_for_date)


@review_router.message(BooksReview.waiting_for_date)
async def get_date(message: types.Message, state: FSMContext):
    if message.text.lower() != "пропустить":
        try:
            visit_date = datetime.strptime(message.text, "%Y-%m-%d").date()
            await state.update_data(visit_date=visit_date)
        except ValueError:
            await message.answer("Некорректный формат даты. Используйте год-месяц-день или напишите 'пропустить'.")
            return
    else:
        await state.update_data(visit_date=None)

    await message.answer("Поставьте нам оценку от 1 до 5:")
    await state.set_state(BooksReview.waiting_for_rate)


@review_router.message(BooksReview.waiting_for_rate)
async def get_rate(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(rate=int(message.text))
        await message.answer("Оставьте дополнительные комментарии:")
        await state.set_state(BooksReview.waiting_for_extra_comments)
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5.")


@review_router.message(BooksReview.waiting_for_extra_comments)
async def finish_review(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    data = await state.get_data()

    review_text = (
        f"Спасибо за ваш отзыв!\n\n"
        f"Имя: {data.get('name')}\n"
        f"Контакт: {data.get('contact')}\n"
        f"Дата посещения: {data.get('visit_date') or 'Не указана'}\n"
        f"Оценка: {data.get('rate')}\n"
        f"Комментарий: {data.get('extra_comments')}"
    )

    db.save_review(
        data.get("name"),
        data.get("contact"),
        data.get("visit_date"),
        data.get("rate"),
        data.get("extra_comments")
    )

    await message.answer(review_text)
    await state.clear()
