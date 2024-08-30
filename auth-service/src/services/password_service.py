from base64 import urlsafe_b64encode
from hashlib import pbkdf2_hmac
from functools import lru_cache

APP_ITERS = 100_000
SALT = "<salt>"


class PasswordService:
    def __init__(self):
        self.salt = SALT
        self.app_iters = APP_ITERS

    def compute_hash(self, password: str):
        password_enc = password.encode('utf-8')
        password_hash_bytes = pbkdf2_hmac('sha256', password_enc, self.salt, self.app_iters)
        password_hash = urlsafe_b64encode(password_hash_bytes).decode('utf-8')
        return password_hash

    def check_password(self, password: str, target_hash: str):
        return self.compute_hash(password) == target_hash


@lru_cache
def get_password_service() -> PasswordService:
    return PasswordService()