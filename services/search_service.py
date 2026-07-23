from dataclasses import dataclass

from models.premise import Premise
from services.premise_service import PremiseService

TYPE_ALIASES = {
    "склад": "склад",
    "складское": "склад",
    "павильон": "торгов",
    "офис": "офис",
    "офисное": "офис",
    "торговое": "торгов",
    "торговое место": "торгов",
}


@dataclass(frozen=True)
class SearchQuery:
    area_max: float | None = None
    price_m2_max: float | None = None
    premise_type: str | None = None


class SearchService:
    def __init__(self, premise_service: PremiseService):
        self.premise_service = premise_service

    def search(self, query: SearchQuery) -> list[Premise]:
        result = self.premise_service.free_list()
        if query.area_max is not None:
            result = [item for item in result if item.area <= query.area_max]
        if query.price_m2_max is not None:
            result = [item for item in result if self._price_m2(item) <= query.price_m2_max]
        if query.premise_type:
            normalized_type = TYPE_ALIASES.get(query.premise_type.lower(), query.premise_type.lower())
            result = [item for item in result if normalized_type in item.type.lower() or normalized_type in item.title.lower()]
        return result

    @staticmethod
    def parse(text: str) -> SearchQuery:
        tokens = text.split()[1:]
        values: dict[str, str] = {}
        for token in tokens:
            if "=" not in token:
                continue
            key, value = token.split("=", 1)
            values[key.lower()] = value.strip().replace(",", ".")

        return SearchQuery(
            area_max=SearchService._float_value(values.get("area") or values.get("площадь")),
            price_m2_max=SearchService._float_value(
                values.get("price_m2") or values.get("м2") or values.get("цена_м2")
            ),
            premise_type=values.get("type") or values.get("тип"),
        )

    @staticmethod
    def is_empty(query: SearchQuery) -> bool:
        return query.area_max is None and query.price_m2_max is None and not query.premise_type

    @staticmethod
    def help_text() -> str:
        return (
            "🔎 Поиск помещений\n\n"
            "Формат: /search area=50 price_m2=900 type=склад\n\n"
            "Параметры:\n"
            "area или площадь — максимальная площадь, м²\n"
            "price_m2 или цена_м2 — максимальная стоимость за м²\n"
            "type или тип — склад, павильон, офисное, торговое\n\n"
            "Примеры:\n"
            "/search type=склад\n"
            "/search area=30 type=павильон\n"
            "/search price_m2=800 type=офисное"
        )

    @staticmethod
    def _float_value(value: str | None) -> float | None:
        if not value:
            return None
        try:
            return float(value)
        except ValueError:
            return None

    @staticmethod
    def _price_m2(premise: Premise) -> float:
        return premise.price / premise.area if premise.area else float("inf")
