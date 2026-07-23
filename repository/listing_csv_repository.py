import csv
from pathlib import Path

from models.listing import Listing


class ListingCsvRepository:
    def __init__(self, filename: str | Path):
        self.filename = Path(filename)

    def get_all(self) -> list[Listing]:
        if not self.filename.exists():
            return []

        with self.filename.open(encoding="utf-8", newline="") as file:
            return [self._row_to_listing(index, row) for index, row in enumerate(csv.DictReader(file), start=1)]

    @staticmethod
    def _row_to_listing(index: int, row: dict[str, str]) -> Listing:
        return Listing(
            id=index,
            title=row.get("title") or row.get("tiitle", ""),
            building=row.get("building", ""),
            price=int(float(row.get("price") or 0)),
            description=row.get("description", ""),
        )
