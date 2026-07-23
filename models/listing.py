from dataclasses import dataclass


@dataclass
class Listing:
    id: int
    title: str
    price: int
    description: str
    building: str = ""
