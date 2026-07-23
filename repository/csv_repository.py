import csv
from pathlib import Path
from models.premise import Premise


class CsvRepository:
    """Read premises from a CSV file and map rows to domain objects."""

    def __init__(self, filename: str | Path):
        self.filename = Path(filename)

    def get_all(self) -> list[Premise]:
        if not self.filename.exists():
            return []

        with self.filename.open(encoding="utf-8", newline="") as file:
            return [self._row_to_premise(row) for row in csv.DictReader(file)]

    def get_free(self) -> list[Premise]:
        return [item for item in self.get_all() if item.status.lower() == "free"]

    def get_by_id(self, item_id: int) -> Premise | None:
        return next((item for item in self.get_all() if item.id == item_id), None)

    @staticmethod
    def _row_to_premise(row: dict[str, str]) -> Premise:
        return Premise(
            id=int(row.get("id", 0)),
            title=row.get("title", ""),
            type=row.get("type", ""),
            building=row.get("building", ""),
            floor=row.get("floor", ""),
            area=float(row.get("area") or 0),
            price=int(float(row.get("price") or 0)),
            description=row.get("description", ""),
            status=row.get("status", ""),
            photo=row.get("photo", ""),
        )
