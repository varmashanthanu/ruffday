from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=f"templates")
TEMPLATES_SUB = "general_pages"
general_pages_router = APIRouter(
    prefix="",
    tags=["home"]

)


@general_pages_router.get("/")
async def home(request: Request):
    user = request.session.get("user") or None
    return templates.TemplateResponse(f"{TEMPLATES_SUB}/home.html", {"request": request, "user": user})
