APPLICATION_STATES: dict[int, dict[str, str]] = {}


def start_application(chat_id: int) -> None:
    APPLICATION_STATES[chat_id] = {"step": "area"}


def get_application(chat_id: int) -> dict[str, str] | None:
    return APPLICATION_STATES.get(chat_id)


def update_application(chat_id: int, key: str, value: str, next_step: str) -> None:
    state = APPLICATION_STATES.setdefault(chat_id, {})
    state[key] = value
    state["step"] = next_step


def clear_application(chat_id: int) -> None:
    APPLICATION_STATES.pop(chat_id, None)
