from __future__ import annotations

from maxapi import Dispatcher
from maxapi.types import Command, MessageCreated

HELP_TEXT = (
    "Доступные команды:\n"
    "/start — зарегистрировать пользователя и начать работу\n"
    "/help — показать эту справку"
)


def register_help_handlers(dp: Dispatcher) -> None:
    @dp.message_created(Command("help"))
    async def handle_help(event: MessageCreated) -> None:
        await event.message.answer(HELP_TEXT)
