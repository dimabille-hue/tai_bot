from maxapi.types import MessageCallback

from handlers.context import premise_service
from keyboards.main_menu import main_keyboard
from keyboards.premise_keyboard import premise_keyboard
from keyboards.premises_list import premises_list_keyboard
from logger import logger

STUB_RESPONSES = {
    "application": "Чтобы подать заявку, выберите помещение и нажмите «Подать заявку» в карточке.",
    "documents": "Раздел документов готовится. Мы добавим файлы и шаблоны в ближайшем обновлении.",
    "contacts": "☎ Контакты АО «ТомскАгроИнвест» будут добавлены администратором бота.",
}


def register_callback_handlers(dp, bot):
    @dp.message_callback()
    async def callback_handler(event: MessageCallback):
        payload = event.callback.payload
        chat_id = event.chat.chat_id
        logger.info("Callback payload: %s", payload)

        if payload == "premises":
            premises = premise_service.free_list()
            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "🏢 Свободные помещения\n\nВыберите интересующее помещение:"
                    if premises
                    else "Свободных помещений сейчас нет."
                ),
                attachments=[premises_list_keyboard(premises)] if premises else [main_keyboard()],
            )
            return

        if payload.startswith("premise_"):
            await send_premise_card(bot, chat_id, payload.removeprefix("premise_"))
            return

        if payload.startswith("apply_"):
            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "📝 Заявка\n\n"
                    "Спасибо за интерес! Напишите ваше имя, телефон и удобное время для связи. "
                    "Менеджер свяжется с вами и уточнит детали."
                ),
            )
            return

        if payload in STUB_RESPONSES:
            await bot.send_message(chat_id=chat_id, text=STUB_RESPONSES[payload])
            return

        logger.warning("Unknown callback payload: %s", payload)


async def send_premise_card(bot, chat_id: int, raw_id: str) -> None:
    try:
        premise_id = int(raw_id)
    except ValueError:
        await bot.send_message(chat_id=chat_id, text="Некорректный идентификатор помещения.")
        return

    premise = premise_service.get(premise_id)
    if not premise:
        await bot.send_message(chat_id=chat_id, text="Помещение не найдено.")
        return

    await bot.send_message(
        chat_id=chat_id,
        text=premise_service.format_card(premise),
        attachments=[premise_keyboard(premise.id)],
    )
