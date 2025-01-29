from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command('start'))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Наш сайт книжного магазина", url="https://"
                                                                                  "bookhouse.kg"),
                types.InlineKeyboardButton(text="Оставить отзыв", callback_data="review:start")

            ]

        ]

    )
    await message.reply(f"Привет, {name}! Добро пожаловать в наш книжный магазин.", reply_markup=kb)
