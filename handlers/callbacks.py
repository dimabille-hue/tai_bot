from maxapi.types import MessageCallback

from handlers.catalog import CATALOG_SECTIONS
from handlers.context import premise_service
from handlers.messages import send_catalog
from keyboards.main_menu import main_keyboard
from keyboards.premise_keyboard import premise_keyboard
from keyboards.premises_list import premises_list_keyboard
from logger import logger
from storage.search_cache import get_search_results

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

        if payload == "main_menu":
            await bot.send_message(chat_id=chat_id, text="Главное меню", attachments=[main_keyboard()])
            return

        if payload in CATALOG_SECTIONS:
            await send_catalog(bot, chat_id, payload)
            return

        if payload.startswith("catalog_"):
            await send_catalog_page(bot, chat_id, payload)
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


async def send_catalog_page(bot, chat_id: int, payload: str) -> None:
    raw = payload.removeprefix("catalog_")
    section_key, _, raw_page = raw.rpartition("_")
    try:
        page = int(raw_page)
    except ValueError:
        page = 0

    if section_key == "search":
        premises = get_search_results(chat_id)
        await bot.send_message(
            chat_id=chat_id,
            text="🔎 Результаты поиска\n\nВыберите объект:" if premises else "Результаты поиска устарели. Выполните /search ещё раз.",
            attachments=[premises_list_keyboard(premises, "search", page)] if premises else [main_keyboard()],
        )
        return

    if section_key not in CATALOG_SECTIONS:
        await bot.send_message(chat_id=chat_id, text="Раздел не найден.", attachments=[main_keyboard()])
        return

    await send_catalog(bot, chat_id, section_key, page)


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
