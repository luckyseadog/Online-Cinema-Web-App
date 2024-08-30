from functools import lru_cache


class AuthorizationVerificationService:
    async def check(self, token: str | None, rigth: str | None): ...


@lru_cache
def get_authorization_verification_service() -> AuthorizationVerificationService:
    return AuthorizationVerificationService()
