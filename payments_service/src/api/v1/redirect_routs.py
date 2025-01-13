from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

redirect_router = APIRouter()
payment_tags_metadata = {"name": "", "description": ""}


@redirect_router.get(
    "/success_response"
)
async def success():
    jinja_env = Environment(loader=FileSystemLoader("templates/"), autoescape=True)
    template = jinja_env.get_template("success.html")
    html_content = template.render()
    return HTMLResponse(content=html_content, status_code=200)


@redirect_router.get(
    "/cancel_response"
)
async def cancel():
    jinja_env = Environment(loader=FileSystemLoader("templates/"), autoescape=True)
    template = jinja_env.get_template("cancel.html")
    html_content = template.render()
    return HTMLResponse(content=html_content, status_code=200)
