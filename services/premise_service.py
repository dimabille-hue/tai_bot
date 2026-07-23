from models.premise import Premise


class PremiseService:
    """Business logic for premises catalog presentation."""

    def __init__(self, repository):
        self.repository = repository

    def free_list(self) -> list[Premise]:
        return self.repository.get_free()

    def get(self, premise_id: int) -> Premise | None:
        return self.repository.get_by_id(premise_id)

    def format_card(self, premise: Premise) -> str:
        rows = [
            f"🏢 {premise.title}",
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

        if premise.description:
            rows.extend(["", f"🚪 {premise.description}"])

        rows.extend(["", "🟢 Свободно"])
        return "\n".join(rows)

    def format_list(self, premises: list[Premise]) -> str:
        if not premises:
            return "Свободных помещений сейчас нет."

        lines = ["🏢 Свободные помещения", ""]
        for item in premises:
            price = f"{item.price:,}".replace(",", " ")
            lines.append(f"{item.id}. {item.title} — {item.area:g} м², {price} ₽/мес")
        return "\n".join(lines)

    def count_free(self) -> int:
        return len(self.free_list())
