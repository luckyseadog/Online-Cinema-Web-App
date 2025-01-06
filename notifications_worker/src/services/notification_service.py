import asyncio
from functools import lru_cache

import aiohttp
from jinja2 import Environment, FileSystemLoader
from src.core.config import settings
from src.models.entity import (
    NewMoviesNotification,
    SaleNotification,
    WelcomeNotification,
)


class InvalidParams(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotificationService:
    def __init__(self):
        self._api_url = settings.api_url
        self._api_key = settings.api_key
        self._jinja_env = Environment(loader=FileSystemLoader("src/templates/"), autoescape=True)

    def _get_payload(self, email: str, subject: str, html_content: str):
        return {
            "sender": {"name": "John Doe", "email": "vasiliydsds@gmail.com"},
            "to": [
                {
                    "name": "John Doe",
                    "email": email,
                }
            ],
            "subject": subject,
            "htmlContent": html_content,
        }

    async def send_welcome(self, template_name: str, params: WelcomeNotification):
        if not isinstance(params, WelcomeNotification):
            raise InvalidParams("You passed invalid params")

        template = self._jinja_env.get_template(template_name)
        html_content = template.render()
        payload = self._get_payload(params.email, params.subject, html_content)

        async with aiohttp.ClientSession() as session:
            headers = {"accept": "application/json", "content-type": "application/json", "api-key": self._api_key}
            async with session.post(self._api_url, json=payload, headers=headers) as resp:
                await resp.json()

    async def send_welcome_many(self, template_name: str, params_batch: list[WelcomeNotification]):
        if not all(isinstance(params, WelcomeNotification) for params in params_batch):
            raise InvalidParams("You passed invalid params")

        tasks = []
        for params in params_batch:
            tasks.append(self.send_welcome(template_name, params))

        await asyncio.gather(*tasks, return_exceptions=True)

    async def send_new_movies(self, template_name: str, params: NewMoviesNotification):
        if not isinstance(params, NewMoviesNotification):
            raise InvalidParams("You passed invalid params")

        template = self._jinja_env.get_template(template_name)
        html_content = template.render(movies=params.movies)
        payload = self._get_payload(params.email, params.subject, html_content)

        async with aiohttp.ClientSession() as session:
            headers = {"accept": "application/json", "content-type": "application/json", "api-key": self._api_key}
            async with session.post(self._api_url, json=payload, headers=headers) as resp:
                await resp.json()

    async def send_new_movies_many(self, template_name: str, params_batch: list[NewMoviesNotification]):
        if not all(isinstance(params, NewMoviesNotification) for params in params_batch):
            raise InvalidParams("You passed invalid params")

        tasks = []
        for params in params_batch:
            tasks.append(self.send_new_movies(template_name, params))

        await asyncio.gather(*tasks, return_exceptions=True)

    async def send_sale(self, template_name: str, params: SaleNotification):
        if not isinstance(params, SaleNotification):
            raise InvalidParams("You passed invalid params")

        template = self._jinja_env.get_template(template_name)
        html_content = template.render()
        payload = self._get_payload(params.email, params.subject, html_content)

        async with aiohttp.ClientSession() as session:
            headers = {"accept": "application/json", "content-type": "application/json", "api-key": self._api_key}
            async with session.post(self._api_url, json=payload, headers=headers) as resp:
                await resp.json()

    async def send_sale_many(self, template_name: str, params_batch: list[SaleNotification]):
        if not all(isinstance(params, SaleNotification) for params in params_batch):
            raise InvalidParams("You passed invalid params")

        tasks = []
        for params in params_batch:
            tasks.append(self.send_sale(template_name, params))

        await asyncio.gather(*tasks, return_exceptions=True)


@lru_cache
def get_notification_service() -> NotificationService:
    return NotificationService()
