from maxapi.types import MessageCreated

from handlers.context import premise_service
from handlers.start import get_message_text
from keyboards.premises_list import premises_list_keyboard


def register_premise_handlers(dp, bot):
    @dp.message_created()
    async def premises_handler(event: MessageCreated):
        if get_message_text(event) != "🏢 Свободные помещения":
            return

        premises = premise_service.free_list()
        await bot.send_message(
            chat_id=event.chat.chat_id,
            text=premise_service.format_list(premises),
            attachments=[premises_list_keyboard(premises)] if premises else None,
        )
