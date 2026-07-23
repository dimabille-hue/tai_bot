import csv
from pathlib import Path


class ContactService:
    def __init__(self, filename: str | Path):
        self.filename = Path(filename)

    def list_contacts(self) -> list[dict[str, str]]:
        if not self.filename.exists():
            return []

        with self.filename.open(encoding="utf-8", newline="") as file:
            return list(csv.DictReader(file))

    def format_contacts(self) -> str:
        contacts = self.list_contacts()
        if not contacts:
            return (
                "☎ Контакты\n\n"
                f"Контакты не настроены. Добавьте строки в `{self.filename}` "
                "с колонками `label,value`."
            )

        lines = ["☎ Контакты", ""]
        for contact in contacts:
            label = contact.get("label", "").strip()
            value = contact.get("value", "").strip()
            if label and value:
                lines.append(f"{label}: {value}")
        return "\n".join(lines)
