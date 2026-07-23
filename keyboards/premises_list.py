from maxapi.types import Attachment

from keyboards.main_menu import keyboard


def premises_list_keyboard(premises) -> Attachment:
    return keyboard(
        [[(f"{item.title} | {item.area:g} м²", f"premise_{item.id}")]]
        for item in premises
    )
