import os
from contextlib import contextmanager
from typing import Iterator

from sqlmodel import Session, SQLModel, create_engine


def _get_database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///./database.db")


engine = create_engine(_get_database_url(), echo=False, pool_pre_ping=True)


def init_db() -> None:
    # Ensure models are imported before creating tables
    from .model import stock  # noqa: F401

    SQLModel.metadata.create_all(engine)


@contextmanager
def session_scope() -> Iterator[Session]:
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session

