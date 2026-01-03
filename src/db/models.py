from __future__ import annotations

from typing import Any

from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    telegram_username: Mapped[str | None] = mapped_column(String(150), nullable=True)
    max_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        unique=True,
        index=True,
    )
    count_messages: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    dialogs: Mapped[list["Dialog"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Dialog(Base):
    __tablename__ = "dialogs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    messages_list: Mapped[list[dict[str, Any]]] = mapped_column(
        MutableList.as_mutable(JSONB),
        default=list,
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates="dialogs")
