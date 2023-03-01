from fastapi import HTTPException, status, APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory=f"templates")
TEMPLATES_SUB = "adoption_fetchers_pages"
adoption_fetchers_pages_router = APIRouter(
    prefix="/adoption_fetchers",
    tags=["adoption_fetchers"]
)


@adoption_fetchers_pages_router.get("/", status_code=status.HTTP_200_OK)
async def home(request: Request):
    """

    Args:
        request:

    Returns:

    """
    
    return templates.TemplateResponse(f"{TEMPLATES_SUB}/adoption_fetchers.html", {"request": request})
