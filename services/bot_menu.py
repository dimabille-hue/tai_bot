from maxapi.types.command import BotCommand

BOT_COMMANDS = (
    BotCommand(name="start", description="Запустить бота"),
    BotCommand(name="menu", description="Открыть главное меню"),
    BotCommand(name="clear", description="Очистить последние сообщения"),
    BotCommand(name="search", description="Поиск помещений"),
    BotCommand(name="help", description="Показать подсказку"),
)


async def setup_bot_commands(bot) -> None:
    await bot.set_my_commands(*BOT_COMMANDS)
