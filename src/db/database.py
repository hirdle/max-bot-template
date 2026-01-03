from __future__ import annotations

from typing import Final

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

import config


def _build_database_url() -> URL:
    missing = []
    if not config.DB_USER:
        missing.append("DB_USER")
    if not config.DB_PASS:
        missing.append("DB_PASS")
    if not config.DB_NAME:
        missing.append("DB_NAME")
    if missing:
        missing_list = ", ".join(missing)
        raise RuntimeError(f"Missing database settings: {missing_list}")

    return URL.create(
        drivername="postgresql+psycopg",
        username=config.DB_USER,
        password=config.DB_PASS,
        host=config.DB_HOST,
        port=int(config.DB_PORT or 5432),
        database=config.DB_NAME,
    )


DATABASE_URL: Final[URL] = _build_database_url()
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db() -> None:
    if not config.DB_AUTO_CREATE:
        return

    from db.models import Base

    Base.metadata.create_all(bind=engine)
