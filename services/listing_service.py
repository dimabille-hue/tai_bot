from models.listing import Listing


class ListingService:
    def __init__(self, repository):
        self.repository = repository

    def list(self) -> list[Listing]:
        return self.repository.get_all()

    def get(self, listing_id: int) -> Listing | None:
        return next((item for item in self.list() if item.id == listing_id), None)

    def format_card(self, listing: Listing, title: str) -> str:
        rows = [f"{title}", "", f"🏷 {listing.title}"]
        if listing.building:
            rows.append(f"📍 {listing.building}")
        rows.append(f"💰 {listing.price:,} ₽/мес".replace(",", " "))
        if listing.description:
            rows.extend(["", f"✨ {listing.description}"])
        return "\n".join(rows)
