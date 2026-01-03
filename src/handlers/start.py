from __future__ import annotations

from maxapi import Dispatcher
from maxapi.types import BotStarted, Command, MessageCreated

from db.models import User
from handlers.user_registration import register_user


def register_start_handlers(dp: Dispatcher) -> None:
    @dp.bot_started()
    async def bot_started(event: BotStarted) -> None:
        await event.bot.send_message(
            chat_id=event.chat_id,
            text="Привет! Отправь мне /start",
        )

    @dp.message_created(Command("start"))
    @register_user
    async def handle_start(event: MessageCreated, user: User) -> None:

        print(user.id, user.first_name, user.telegram_id)
        await event.message.answer("Добро пожаловать! Вы успешно зарегистрированы.")
