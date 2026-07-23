from maxapi.types import MessageCreated

from keyboards.main_menu import main_keyboard

WELCOME_TEXT = (
    "Здравствуйте!\n\n"
    "Бот аренды помещений\n"
    "АО «ТомскАгроИнвест»\n\n"
    "Выберите нужный раздел:"
)


def get_message_text(event: MessageCreated) -> str:
    body = getattr(event.message, "body", None)
    return (getattr(body, "text", None) or "").strip()


def register_start_handlers(dp, bot):
    @dp.message_created()
    async def start_handler(event: MessageCreated):
        if get_message_text(event) != "/start":
            return

        await bot.send_message(
            chat_id=event.chat.chat_id,
            text=WELCOME_TEXT,
            attachments=[main_keyboard()],
        )
