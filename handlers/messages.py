from maxapi.types import MessageCreated

from handlers.catalog import CATALOG_SECTIONS
from handlers.commands import HELP_TEXT
from handlers.context import premise_service
from handlers.start import WELCOME_TEXT, get_message_text
from keyboards.main_menu import main_keyboard
from keyboards.premises_list import premises_list_keyboard
from services.chat_cleanup_service import ChatCleanupService
from services.search_service import SearchService
from storage.search_cache import set_search_results

TEXT_TO_SECTION = {
    "🏢 Свободные помещения": "premises",
    "🛒 Свободные торговые места": "trade_places",
    "🔥 Специальные предложения": "special_offers",
}


def register_message_handlers(dp, bot):
    cleanup_service = ChatCleanupService(bot)
    search_service = SearchService(premise_service)

    @dp.message_created()
    async def message_handler(event: MessageCreated):
        text = get_message_text(event)
        command = text.lower()
        chat_id = event.chat.chat_id

        if command in {"/start", "/menu"}:
            await bot.send_message(chat_id=chat_id, text=WELCOME_TEXT, attachments=[main_keyboard()])
            return

        if command == "/help":
            await bot.send_message(chat_id=chat_id, text=HELP_TEXT, attachments=[main_keyboard()])
            return

        if command == "/clear":
            deleted_count = await cleanup_service.clear_recent_messages(chat_id)
            await bot.send_message(
                chat_id=chat_id,
                text=f"🧹 Очистка завершена. Удалено сообщений: {deleted_count}.",
                attachments=[main_keyboard()],
            )
            return

        if command.startswith("/search"):
            await send_search_results(bot, chat_id, text, search_service)
            return

        section_key = TEXT_TO_SECTION.get(text)
        if section_key:
            await send_catalog(bot, chat_id, section_key)


async def send_catalog(bot, chat_id: int, section_key: str, page: int = 0) -> None:
    title, empty_text, loader = CATALOG_SECTIONS[section_key]
    premises = loader()
    await bot.send_message(
        chat_id=chat_id,
        text=f"{title}\n\nВыберите объект:" if premises else empty_text,
        attachments=[premises_list_keyboard(premises, section_key, page)] if premises else [main_keyboard()],
    )


async def send_search_results(bot, chat_id: int, text: str, search_service: SearchService) -> None:
    query = search_service.parse(text)
    if search_service.is_empty(query):
        await bot.send_message(chat_id=chat_id, text=search_service.help_text(), attachments=[main_keyboard()])
        return

    premises = search_service.search(query)
    set_search_results(chat_id, premises)
    await bot.send_message(
        chat_id=chat_id,
        text="🔎 Результаты поиска\n\nВыберите объект:" if premises else "По вашему запросу ничего не найдено.",
        attachments=[premises_list_keyboard(premises, "search", 0)] if premises else [main_keyboard()],
    )
