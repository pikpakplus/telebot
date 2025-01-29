from aiogram import Router, types
from aiogram.filters import Command

my_info_router = Router()


@my_info_router.message(Command('myinfo'))
async def myinfo_handler(message: types.Message):
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    username = user.username
    response = (
        f"Ваш ID: {user_id}\n"
        f"Ваше имя: {first_name}\n"
        f"Ваш username: @{username if username else 'не указан'}")
    await message.answer(response)
