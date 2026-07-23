from collections.abc import Callable

from models.premise import Premise

CatalogLoader = Callable[[], list[Premise]]

CATALOG_SECTIONS: dict[str, tuple[str, str, CatalogLoader]] = {}


def register_catalog_sections(premise_service) -> None:
    CATALOG_SECTIONS.clear()
    CATALOG_SECTIONS.update(
        {
            "premises": (
                "🏢 Свободные помещения",
                "Свободных помещений сейчас нет.",
                premise_service.free_list,
            ),
            "trade_places": (
                "🛒 Свободные торговые места",
                "Свободных торговых мест сейчас нет.",
                premise_service.free_trade_list,
            ),
            "special_offers": (
                "🔥 Специальные предложения",
                "Специальных предложений сейчас нет.",
                premise_service.special_offers,
            ),
        }
    )
