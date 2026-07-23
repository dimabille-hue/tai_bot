from collections.abc import Callable
from typing import Any

CatalogLoader = Callable[[], list[Any]]
CardFormatter = Callable[[Any], str]

CATALOG_SECTIONS: dict[str, dict[str, Any]] = {}


def register_catalog_sections(premise_service, trade_place_service, special_offer_service) -> None:
    CATALOG_SECTIONS.clear()
    CATALOG_SECTIONS.update(
        {
            "premises": {
                "title": "🏢 Свободные помещения",
                "empty_text": "Свободных помещений сейчас нет.",
                "loader": premise_service.free_list,
                "card": premise_service.format_card,
            },
            "trade_places": {
                "title": "🛒 Свободные торговые места",
                "empty_text": "Свободных торговых мест сейчас нет.",
                "loader": trade_place_service.list,
                "card": lambda item: trade_place_service.format_card(item, "🛒 Свободное торговое место"),
            },
            "special_offers": {
                "title": "🔥 Специальные предложения",
                "empty_text": "Специальных предложений сейчас нет.",
                "loader": special_offer_service.list,
                "card": lambda item: special_offer_service.format_card(item, "🔥 Специальное предложение"),
            },
        }
    )
