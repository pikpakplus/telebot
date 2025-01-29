from aiogram import Router, types
from aiogram.filters import Command
import random

random_name_router = Router()

Names = ("Tokito", "Xan", "Alex", "Hamura", "2Pac", "Ronaldo")


@random_name_router.message(Command('random'))
async def random_name_handler(message: types.Message):
    random_name = random.choice(Names)
    await message.answer(f"рандомное имя: {random_name}")