from models.premise import Premise

_search_results: dict[int, list[Premise]] = {}


def set_search_results(chat_id: int, premises: list[Premise]) -> None:
    _search_results[chat_id] = premises


def get_search_results(chat_id: int) -> list[Premise]:
    return _search_results.get(chat_id, [])


def clear_search_results(chat_id: int | None = None) -> None:
    if chat_id is None:
        _search_results.clear()
        return
    _search_results.pop(chat_id, None)
