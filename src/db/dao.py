from __future__ import annotations

from typing import Any

from sqlalchemy import select

from db.base_dao import BaseDAO
from db.models import Dialog, User


class UserDAO(BaseDAO[User]):
    model = User

    def get_by_max_id(self, max_id: int) -> User | None:
        with self._session_scope() as session:
            stmt = select(User).where(User.max_id == max_id)
            return session.scalar(stmt)

    def get_by_telegram_username(self, telegram_username: str) -> User | None:
        with self._session_scope() as session:
            stmt = select(User).where(User.telegram_username == telegram_username)
            return session.scalar(stmt)

    def increment_message_count(self, user_id: int, delta: int = 1) -> User | None:
        with self._session_scope() as session:
            user = session.get(User, user_id)
            if user is None:
                return None
            user.count_messages += delta
            session.flush()
            session.refresh(user)
            return user


class DialogDAO(BaseDAO[Dialog]):
    model = Dialog

    def get_by_user_id(self, user_id: int) -> list[Dialog]:
        with self._session_scope() as session:
            stmt = select(Dialog).where(Dialog.user_id == user_id)
            return list(session.scalars(stmt).all())

    def append_message(self, dialog_id: int, message: dict[str, Any]) -> Dialog | None:
        with self._session_scope() as session:
            dialog = session.get(Dialog, dialog_id)
            if dialog is None:
                return None
            dialog.messages_list.append(message)
            session.flush()
            session.refresh(dialog)
            return dialog
