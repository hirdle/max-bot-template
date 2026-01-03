from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Generator, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from db.database import SessionLocal
from db.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseDAO(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, session_factory: sessionmaker = SessionLocal) -> None:
        self._session_factory = session_factory

    @contextmanager
    def _session_scope(self) -> Generator[Session, None, None]:
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create(self, **data: Any) -> ModelType:
        with self._session_scope() as session:
            obj = self.model(**data)
            session.add(obj)
            session.flush()
            session.refresh(obj)
            return obj

    def get_by_id(self, obj_id: int) -> ModelType | None:
        with self._session_scope() as session:
            return session.get(self.model, obj_id)

    def get_all(self) -> list[ModelType]:
        with self._session_scope() as session:
            return list(session.scalars(select(self.model)).all())

    def update(self, obj_id: int, **data: Any) -> ModelType | None:
        with self._session_scope() as session:
            obj = session.get(self.model, obj_id)
            if obj is None:
                return None
            for key, value in data.items():
                setattr(obj, key, value)
            session.flush()
            session.refresh(obj)
            return obj

    def delete(self, obj_id: int) -> bool:
        with self._session_scope() as session:
            obj = session.get(self.model, obj_id)
            if obj is None:
                return False
            session.delete(obj)
            return True
