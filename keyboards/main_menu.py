from maxapi.types import Attachment, ButtonsPayload, CallbackButton


def keyboard(buttons: list[list[tuple[str, str]]]) -> Attachment:
    return Attachment(
        type="inline_keyboard",
        payload=ButtonsPayload(
            buttons=[
                [CallbackButton(text=text, payload=payload) for text, payload in row]
                for row in buttons
            ]
        ),
    )


def main_keyboard() -> Attachment:
    return keyboard(
        [
            [("🏢 Свободные помещения", "premises")],
            [("🛒 Свободные торговые места", "trade_places")],
            [("🔥 Специальные предложения", "special_offers")],
            [("📝 Подать заявку", "application")],
            [("📄 Документы", "documents")],
            [("☎ Контакты", "contacts")],
        ]
    )
