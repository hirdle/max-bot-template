from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable

from maxapi.types import MessageCreated

from db.dao import UserDAO
from db.models import User

logger = logging.getLogger(__name__)


def register_user(
    handler: Callable[..., Awaitable[None]],
) -> Callable[..., Awaitable[None]]:
    async def wrapper(event: MessageCreated, *args: Any, **kwargs: Any) -> None:
        user = _get_or_register_user(event)
        if user is None:
            message = getattr(event, "message", None)
            if message is not None:
                await message.answer("Привет! Не получилось зарегистрировать вас.")
            return

        await handler(event, user, *args, **kwargs)

    return wrapper


def _get_or_register_user(event: MessageCreated) -> User | None:
    sender = event.message.sender
    user_id = sender.user_id
    first_name = sender.first_name
    last_name = sender.last_name
    username = sender.username

    if user_id is None:
        logger.warning("Не удалось определить идентификатор пользователя.")
        return None

    payload = {
        "max_id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "telegram_username": username,
    }

    user_dao = UserDAO()
    existing = user_dao.get_by_max_id(int(user_id))
    if existing is not None:
        return existing

    payload["max_id"] = int(user_id)
    return user_dao.create(**payload)
