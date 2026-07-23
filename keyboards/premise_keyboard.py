from maxapi.types import Attachment

from keyboards.main_menu import keyboard


def premise_keyboard(premise_id: int) -> Attachment:
    return keyboard(
        [
            [("📝 Подать заявку", f"apply_{premise_id}")],
            [("⬅ К списку помещений", "premises")],
        ]
    )
