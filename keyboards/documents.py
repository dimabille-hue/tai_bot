from pathlib import Path

from maxapi.types import Attachment

from keyboards.main_menu import keyboard


def documents_keyboard(documents: list[Path]) -> Attachment:
    buttons = [
        [(f"📄 {document.name}", f"document_{index}")]
        for index, document in enumerate(documents)
    ]
    buttons.append([("🏠 Главное меню", "main_menu")])
    return keyboard(buttons)
