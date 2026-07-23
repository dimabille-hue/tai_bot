import csv
from datetime import datetime
from pathlib import Path

APPLICATION_FIELDS = ("data", "area", "price", "description")


class ApplicationService:
    def __init__(self, filename: str | Path):
        self.filename = Path(filename)
        self.filename.parent.mkdir(parents=True, exist_ok=True)

    def save(self, area: str, price: str, description: str) -> None:
        is_new = not self.filename.exists() or self.filename.stat().st_size == 0
        with self.filename.open("a", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=APPLICATION_FIELDS)
            if is_new:
                writer.writeheader()
            writer.writerow(
                {
                    "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "area": area,
                    "price": price,
                    "description": description,
                }
            )
