from collections.abc import Iterable
from typing import Any

from logger import logger


class ChatCleanupService:
    """Delete recent chat messages available through MAX Bot API history."""

    def __init__(self, bot, batch_size: int = 50):
        self.bot = bot
        self.batch_size = batch_size

    async def clear_recent_messages(self, chat_id: int) -> int:
        messages = await self.bot.get_messages(chat_id=chat_id, count=self.batch_size)
        deleted_count = 0

        for message_id in self._message_ids(messages):
            try:
                await self.bot.delete_message(message_id)
                deleted_count += 1
            except Exception as exc:  # noqa: BLE001 - keep cleanup best-effort for old/protected messages.
                logger.warning("Cannot delete message %s in chat %s: %s", message_id, chat_id, exc)

        return deleted_count

    @classmethod
    def _message_ids(cls, response: Any) -> list[str]:
        if response is None:
            return []

        if isinstance(response, dict):
            candidates = response.get("messages", response.get("items", []))
        else:
            candidates = getattr(response, "messages", getattr(response, "items", response))

        if not isinstance(candidates, Iterable) or isinstance(candidates, (str, bytes)):
            return []

        result: list[str] = []
        for message in candidates:
            message_id = cls._message_id(message)
            if message_id:
                result.append(str(message_id))
        return result

    @staticmethod
    def _message_id(message: Any) -> str | None:
        if isinstance(message, dict):
            return message.get("message_id") or message.get("id")
        return getattr(message, "message_id", None) or getattr(message, "id", None)
