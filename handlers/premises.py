from maxapi.types import MessageCreated

from handlers.catalog import CATALOG_SECTIONS
from handlers.context import premise_service
from handlers.start import get_message_text
from keyboards.premises_list import premises_list_keyboard

TEXT_TO_SECTION = {
    "🏢 Свободные помещения": "premises",
    "🛒 Свободные торговые места": "trade_places",
    "🔥 Специальные предложения": "special_offers",
}


def register_premise_handlers(dp, bot):
    @dp.message_created()
    async def premises_handler(event: MessageCreated):
        section_key = TEXT_TO_SECTION.get(get_message_text(event))
        if not section_key:
            return

        title, empty_text, loader = CATALOG_SECTIONS[section_key]
        premises = loader()
        await bot.send_message(
            chat_id=event.chat.chat_id,
            text=premise_service.format_list(premises, title) if premises else empty_text,
            attachments=[premises_list_keyboard(premises)] if premises else None,
        )
