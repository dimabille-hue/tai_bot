from dataclasses import dataclass


@dataclass
class Premise:

    id: int

    title: str

    type: str

    building: str

    floor: str

    area: float

    price: int

    description: str

    status: str

    photo: str = ""