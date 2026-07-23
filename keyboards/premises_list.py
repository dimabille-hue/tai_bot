from collections.abc import Iterable

from maxapi.types import Attachment

from keyboards.main_menu import keyboard
from models.premise import Premise


def premises_list_keyboard(premises: Iterable[Premise]) -> Attachment:
    return keyboard(
        [
            [(f"{item.title} | {item.area:g} м²", f"premise_{item.id}")]
            for item in premises
        ]
    )
