import os
from base64 import urlsafe_b64decode, urlsafe_b64encode
from functools import lru_cache
from hashlib import pbkdf2_hmac
from typing import NamedTuple

from core.config import configs


class Password(NamedTuple):
    hash_name: str
    iters: int
    salt: str
    password_hash: str


class PasswordService:
    def compute_hash(
        self,
        password: str,
        hash_name: str = configs.hash_name_password,
        iters: int = configs.iters_password,
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

    def check_password(self, password: str, target_hash: Password) -> bool:
        return (
            self.compute_hash(password, target_hash.hash_name, target_hash.iters, target_hash.salt).password_hash
            == target_hash.password_hash
        )


@lru_cache
def get_password_service() -> PasswordService:
    return PasswordService()
