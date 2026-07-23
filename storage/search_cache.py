from models.premise import Premise

_search_results: dict[int, list[Premise]] = {}


def set_search_results(chat_id: int, premises: list[Premise]) -> None:
    _search_results[chat_id] = premises


def get_search_results(chat_id: int) -> list[Premise]:
    return _search_results.get(chat_id, [])
