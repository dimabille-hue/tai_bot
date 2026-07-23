from collections.abc import Iterable
from math import ceil
from typing import Any

from maxapi.types import Attachment

from keyboards.main_menu import keyboard

PAGE_SIZE = 5


def premises_list_keyboard(
    items: Iterable[Any],
    section_key: str = "premises",
    page: int = 0,
    page_size: int = PAGE_SIZE,
) -> Attachment:
    catalog_items = list(items)
    pages_count = max(1, ceil(len(catalog_items) / page_size))
    page = max(0, min(page, pages_count - 1))
    page_items = catalog_items[page * page_size : (page + 1) * page_size]

    buttons = [[(button_text(item), f"item_{section_key}_{item.id}")] for item in page_items]

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


def button_text(item: Any) -> str:
    title = getattr(item, "title", "Объект")
    price = getattr(item, "price", 0)
    area = getattr(item, "area", None)
    special = "🔥 " if getattr(item, "special_offer", False) else ""
    if area:
        return f"{special}{title} | {area:g} м² | {price_m2(item):g} ₽/м²"
    return f"{special}{title} | {price:,} ₽/мес".replace(",", " ")


def price_m2(item: Any) -> int:
    area = getattr(item, "area", 0)
    price = getattr(item, "price", 0)
    return round(price / area) if area else 0
