import os
from base64 import urlsafe_b64decode, urlsafe_b64encode
from collections.abc import Callable, Coroutine
from hashlib import pbkdf2_hmac
from typing import Any, NamedTuple

import pytest_asyncio

from core.settings import test_settings


class Password(NamedTuple):
    hash_name: str
    iters: int
    salt: str
    password_hash: str


@pytest_asyncio.fixture(name="compute_hash")  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
def compute_hash() -> Callable[..., Coroutine[Any, Any, Password]]:
    async def inner(
        password: str,
        hash_name: str = test_settings.hash_name_password,
        iters: int = test_settings.iters_password,
        salt: str | None = None,
    ) -> Password:
        if salt is None:
            salt_ = os.urandom(32)
            salt = urlsafe_b64encode(salt_).decode("utf-8")
        else:
            salt_ = urlsafe_b64decode(salt)

        password_hash_bytes = pbkdf2_hmac(hash_name, password.encode("utf-8"), salt_, iters)
        return Password(
            hash_name=hash_name,
            iters=iters,
            salt=salt,
            password_hash=urlsafe_b64encode(password_hash_bytes).decode("utf-8"),
        )

    return inner
