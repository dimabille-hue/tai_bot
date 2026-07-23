from collections.abc import Iterable
from math import ceil

from maxapi.types import Attachment

from keyboards.main_menu import keyboard
from models.premise import Premise

PAGE_SIZE = 5


def premises_list_keyboard(
    premises: Iterable[Premise],
    section_key: str = "premises",
    page: int = 0,
    page_size: int = PAGE_SIZE,
) -> Attachment:
    items = list(premises)
    pages_count = max(1, ceil(len(items) / page_size))
    page = max(0, min(page, pages_count - 1))
    page_items = items[page * page_size : (page + 1) * page_size]

    buttons = [
        [(f"{item.title} | {item.area:g} м² | {price_m2(item):g} ₽/м²", f"premise_{item.id}")]
        for item in page_items
    ]

    if pages_count > 1:
        nav = []
        if page > 0:
            nav.append(("⬅ Назад", f"catalog_{section_key}_{page - 1}"))
        nav.append((f"{page + 1}/{pages_count}", f"catalog_{section_key}_{page}"))
        if page < pages_count - 1:
            nav.append(("Вперёд ➡", f"catalog_{section_key}_{page + 1}"))
        buttons.append(nav)

    buttons.append([("🏠 Главное меню", "main_menu")])
    return keyboard(buttons)


def price_m2(premise: Premise) -> int:
    return round(premise.price / premise.area) if premise.area else 0
