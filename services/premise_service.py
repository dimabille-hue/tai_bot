from models.premise import Premise


class PremiseService:
    """Business logic for premises catalog presentation."""

    def __init__(self, repository):
        self.repository = repository

    def free_list(self) -> list[Premise]:
        return self.repository.get_free()

    def free_trade_list(self) -> list[Premise]:
        return [item for item in self.free_list() if "торгов" in item.type.lower()]

    def special_offers(self) -> list[Premise]:
        return [item for item in self.free_list() if item.special_offer]

    def get(self, premise_id: int) -> Premise | None:
        return self.repository.get_by_id(premise_id)

    def format_card(self, premise: Premise) -> str:
        prefix = "🔥🔥 СПЕЦПРЕДЛОЖЕНИЕ 🔥🔥\n" if premise.special_offer else ""
        rows = [
            f"{prefix}🏢 {premise.title}",
            "",
            f"📐 {premise.area:g} м²",
            f"💰 {premise.price:,} ₽/мес".replace(",", " "),
        ]

        optional_rows = [
            (premise.type, "🏷 Тип: {}"),
            (premise.building, "📍 {}"),
            (premise.floor, "🏬 Этаж: {}"),
        ]
        rows.extend(template.format(value) for value, template in optional_rows if value)

        if premise.special_offer:
            rows.extend(["", "🔥 Специальное предложение"])

        if premise.description:
            rows.extend(["", f"🚪 {premise.description}"])

        rows.extend(["", "🟢 Свободно"])
        return "\n".join(rows)

    def format_list(self, premises: list[Premise], title: str = "🏢 Свободные помещения") -> str:
        if not premises:
            return "В этом разделе сейчас нет свободных объектов."

        lines = [title, ""]
        for item in premises:
            price = f"{item.price:,}".replace(",", " ")
            marker = "🔥 " if item.special_offer else ""
            lines.append(f"{item.id}. {marker}{item.title} — {item.area:g} м², {price} ₽/мес")
        return "\n".join(lines)

    def count_free(self) -> int:
        return len(self.free_list())
