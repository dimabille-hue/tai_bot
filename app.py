import asyncio

from maxapi import Bot, Dispatcher

from config import BOT_TOKEN
from handlers.callbacks import register_callback_handlers
from handlers.messages import register_message_handlers
from logger import logger
from services.bot_menu import setup_bot_commands


def create_dispatcher(bot: Bot) -> Dispatcher:
    dp = Dispatcher()
    register_message_handlers(dp, bot)
    register_callback_handlers(dp, bot)
    return dp


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    dp = create_dispatcher(bot)
    await setup_bot_commands(bot)
    logger.info("BOT STARTED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
