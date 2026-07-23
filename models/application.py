from dataclasses import dataclass
from datetime import datetime


@dataclass
class Application:

    created_at: str

    user_id: str

    name: str

    phone: str

    premise_id: int

    premise_title: str

    comment: str


    @staticmethod
    def create(
        user_id,
        name,
        phone,
        premise,
        comment
    ):

        return Application(

            created_at=datetime.now()
                .strftime("%Y-%m-%d %H:%M:%S"),

            user_id=str(user_id),

            name=name,

            phone=phone,

            premise_id=premise.id,

            premise_title=premise.title,

            comment=comment
        )