from maxapi.types import MessageCallback

from handlers.catalog import CATALOG_SECTIONS
from handlers.context import contact_service, document_service, premise_service
from handlers.messages import send_catalog, start_application_form
from keyboards.main_menu import main_keyboard
from keyboards.premise_keyboard import premise_keyboard
from keyboards.premises_list import premises_list_keyboard
from logger import logger
from storage.search_cache import get_search_results



def register_callback_handlers(dp, bot):
    @dp.message_callback()
    async def callback_handler(event: MessageCallback):
        payload = event.callback.payload
        chat_id = event.chat.chat_id
        logger.info("Callback payload: %s", payload)

        if payload == "main_menu":
            await bot.send_message(chat_id=chat_id, text="Главное меню", attachments=[main_keyboard()])
            return

        if payload == "application":
            await start_application_form(bot, chat_id)
            return

        if payload == "documents":
            await bot.send_message(chat_id=chat_id, text=document_service.format_documents(), attachments=[main_keyboard()])
            return

        if payload == "contacts":
            await bot.send_message(chat_id=chat_id, text=contact_service.format_contacts(), attachments=[main_keyboard()])
            return

        if payload in CATALOG_SECTIONS:
            await send_catalog(bot, chat_id, payload)
            return

        if payload.startswith("catalog_"):
            await send_catalog_page(bot, chat_id, payload)
            return

        if payload.startswith("item_"):
            await send_item_card(bot, chat_id, payload)
            return

        if payload.startswith("premise_"):
            await send_premise_card(bot, chat_id, payload.removeprefix("premise_"))
            return

        if payload.startswith("apply_"):
            await start_application_form(bot, chat_id)
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


async def send_item_card(bot, chat_id: int, payload: str) -> None:
    raw = payload.removeprefix("item_")
    section_key, _, raw_id = raw.rpartition("_")
    if section_key == "search":
        await send_premise_card(bot, chat_id, raw_id)
        return
    if section_key not in CATALOG_SECTIONS:
        await bot.send_message(chat_id=chat_id, text="Раздел не найден.", attachments=[main_keyboard()])
        return

    try:
        item_id = int(raw_id)
    except ValueError:
        await bot.send_message(chat_id=chat_id, text="Некорректный идентификатор.")
        return

    section = CATALOG_SECTIONS[section_key]
    item = next((catalog_item for catalog_item in section["loader"]() if catalog_item.id == item_id), None)
    if not item:
        await bot.send_message(chat_id=chat_id, text="Объект не найден.", attachments=[main_keyboard()])
        return

    attachments = [premise_keyboard(item.id)] if section_key == "premises" else [main_keyboard()]
    await bot.send_message(chat_id=chat_id, text=section["card"](item), attachments=attachments)


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
