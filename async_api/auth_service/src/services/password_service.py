import os
from base64 import urlsafe_b64encode
from hashlib import pbkdf2_hmac

SALT = os.environ.get('SAULT', '<salt>').encode('utf-8')
APP_ITERS = int(os.environ.get('APP_ITERS', 100_000))


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


password_service = PasswordService()
