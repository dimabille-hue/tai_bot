from maxapi.types import MessageCreated

from handlers.start import WELCOME_TEXT, get_message_text
from keyboards.main_menu import main_keyboard
from services.chat_cleanup_service import ChatCleanupService

HELP_TEXT = (
    "Команды бота:\n\n"
    "/start — открыть главное меню\n"
    "/menu — показать меню разделов\n"
    "/clear — очистить последние сообщения в чате\n"
    "/help — показать подсказку"
)


def register_command_handlers(dp, bot):
    cleanup_service = ChatCleanupService(bot)

    @dp.message_created()
    async def command_handler(event: MessageCreated):
        text = get_message_text(event).lower()
        chat_id = event.chat.chat_id

        if text == "/menu":
            await bot.send_message(chat_id=chat_id, text=WELCOME_TEXT, attachments=[main_keyboard()])
            return

        if text == "/help":
            await bot.send_message(chat_id=chat_id, text=HELP_TEXT, attachments=[main_keyboard()])
            return

        if text == "/clear":
            deleted_count = await cleanup_service.clear_recent_messages(chat_id)
            await bot.send_message(
                chat_id=chat_id,
                text=f"🧹 Очистка завершена. Удалено сообщений: {deleted_count}.",
                attachments=[main_keyboard()],
            )
