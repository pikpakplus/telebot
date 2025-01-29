import asyncio
import logging
from handlers.start import start_router
from handlers.echo_messege import other_router
from bot_config import bot, dp
from handlers.info import my_info_router
from handlers.name_random import random_name_router
from handlers.review import review_router
from handlers.book_admin import book_admin_router
from handlers.show_book import show_books_router


async def main():
    dp.include_router(start_router)
    dp.include_router(my_info_router)
    dp.include_router(random_name_router)
    dp.include_router(review_router)
    dp.include_router(book_admin_router)
    dp.include_router(show_books_router)
    dp.include_router(other_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
