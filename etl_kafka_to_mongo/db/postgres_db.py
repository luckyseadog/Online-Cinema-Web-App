from collections.abc import Generator
from functools import lru_cache
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.config import configs


engine_admin = create_engine(configs.postgres_dsn_admin)


@lru_cache
def get_session_admin() -> Generator[Session, Any, None]:
    with Session(engine_admin) as session_admin:
        yield session_admin
