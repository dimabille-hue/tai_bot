import csv
from datetime import datetime
from pathlib import Path

APPLICATION_FIELDS = ("data", "user_id", "area", "price", "phone", "description")


class ApplicationService:
    def __init__(self, filename: str | Path):
        self.filename = Path(filename)
        self.filename.parent.mkdir(parents=True, exist_ok=True)

    def save(self, user_id: int | str, area: str, price: str, phone: str, description: str) -> None:
        is_new = not self.filename.exists() or self.filename.stat().st_size == 0
        with self.filename.open("a", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=APPLICATION_FIELDS)
            if is_new:
                writer.writeheader()
            writer.writerow(
                {
                    "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "user_id": str(user_id),
                    "area": area,
                    "price": price,
                    "phone": phone,
                    "description": description,
                }
            )

    def list_by_user(self, user_id: int | str) -> list[dict[str, str]]:
        if not self.filename.exists():
            return []

        with self.filename.open(encoding="utf-8", newline="") as file:
            return [
                row
                for row in csv.DictReader(file)
                if row.get("user_id") == str(user_id)
            ]

    def format_archive(self, user_id: int | str) -> str:
        applications = self.list_by_user(user_id)
        if not applications:
            return "📦 Архив заявок\n\nУ вас пока нет сохранённых заявок."

        lines = ["📦 Архив заявок", ""]
        for index, item in enumerate(applications, start=1):
            lines.extend(
                [
                    f"{index}. {item.get('data', 'без даты')}",
                    f"📐 Площадь: {item.get('area', '-')}",
                    f"💰 Бюджет: {item.get('price', '-')}",
                    f"☎ Контакт: {item.get('phone', '-')}",
                    f"📝 Описание: {item.get('description', '-')}",
                    "",
                ]
            )
        return "\n".join(lines).strip()
