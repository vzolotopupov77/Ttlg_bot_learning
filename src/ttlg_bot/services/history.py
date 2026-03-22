"""In-memory хранение истории диалога (без БД на MVP)."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence


class HistoryStore:
    """Хранит последние сообщения по user_id в памяти процесса."""

    def __init__(self, depth: int = 20) -> None:
        self._depth = depth
        self._by_user: dict[int, list[dict[str, str]]] = defaultdict(list)

    def add(self, user_id: int, role: str, content: str) -> None:
        messages = self._by_user[user_id]
        messages.append({"role": role, "content": content})
        if len(messages) > self._depth:
            del messages[: len(messages) - self._depth]

    def get(self, user_id: int) -> list[dict[str, str]]:
        return list(self._by_user[user_id])

    def pop_last(self, user_id: int) -> None:
        """Удалить последнее сообщение (например при ошибке LLM после add user)."""
        msgs = self._by_user[user_id]
        if msgs:
            msgs.pop()

    def messages_for_api(self, user_id: int) -> Sequence[dict[str, str]]:
        """Сообщения в формате для chat.completions (без system — он добавляется отдельно)."""
        return [m for m in self._by_user[user_id] if m["role"] in ("user", "assistant")]
