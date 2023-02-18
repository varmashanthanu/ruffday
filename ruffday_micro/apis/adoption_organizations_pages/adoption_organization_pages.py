from typing import Dict
from urllib.error import HTTPError
from core.config import Settings
from models import AdoptionOrganizations
from fastapi import HTTPException, status, APIRouter, Request

from models.shared import ListingTypes
from utils import DatabaseManager
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory=f"templates")
TEMPLATES_SUB = "adoption_organizations_pages"
adoption_organization_pages_router = APIRouter(
    prefix="/adoption_organizations",
    tags=["adoption_organizations"]
)


db_name = Settings.ORGANIZATIONS_DB_NAME


def get_organizations_from_db(params: dict = None):
    query_params = {
        "listing_type": ListingTypes.ORGANIZATIONS.value
    }
    if params:
        query_params.update({"address": params})

    all_adoption_organizations = DatabaseManager.search_db(
        db_name=db_name,
        search_params=query_params
    )
    adoption_organizations = [AdoptionOrganizations(**adoption_organization) for adoption_organization in all_adoption_organizations.items]

    return adoption_organizations


@adoption_organization_pages_router.get("/", status_code=status.HTTP_200_OK)
async def home(request: Request):
    """

    Args:
        request:

    Returns:

    """
    adoption_organizations = get_organizations_from_db(params=request.query_params.get("searchValue"))

    return templates.TemplateResponse(f"{TEMPLATES_SUB}/adoption_organizations.html", {"request": request, "adoption_organizations": adoption_organizations})


@adoption_organization_pages_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_adoption_organizations(
    adoption_organization: AdoptionOrganizations,
    request: Request,
):
    """
    An endpoint to create a new organization
    Args:
        adoption_organization (dict): a Dict containing the details of a new adoption listing
        request: request object
    Returns:
        a json object with the details of the new listing on successful creation, else 424 error

    Raises:
        HTTPException 409 or 424 on failed creation
    """
    if form := request.form():
        try:
            new_adoption_organization = adoption_organization.save()

            return new_adoption_organization
        except HTTPError as e:
            raise HTTPException(status_code=e.code, detail=e.reason)

        except Exception as e:
            raise HTTPException(status_code=424, detail=f"Could not add listing due to: {e}")

    else:
        return templates.TemplateResponse(f"{TEMPLATES_SUB}/new_adoption_organization.html")


@adoption_organization_pages_router.post("/search", status_code=status.HTTP_200_OK)
async def get_all_adoption_organizations(
    request: Request,
    search_params: Dict = None,
):
    """
    An Endpoint to search or get all listed adoption details
    Args:
        request (Request): Request object
        search_params: Name of the available adoption

    Returns:
         a json object of all available listings
    """
    adoption_organizations = DatabaseManager.search_db(
        db_name=db_name,
        search_params=search_params
    )

    if adoption_organizations.count:
        return templates.TemplateResponse(f"{TEMPLATES_SUB}/adoption_organizations.html", {"request": request, "adoption_organizations": adoption_organizations.items})
    else:
        return {"message": f"Nothing to see here..."}


@adoption_organization_pages_router.get("/{organization_id}", status_code=status.HTTP_200_OK)
async def get_adoption_organizations(adoption_organization_id: str):
    """
    Endpoint to get a single adoption organization by ID
    Args:
        adoption_organization_id:

    Returns:

    """
    adoption_organization = DatabaseManager.read_from_db(
        db_name=db_name,
        key=adoption_organization_id)
    return adoption_organization if adoption_organization else HTTPException(
        status_code=404, detail=f"No listing found for {adoption_organization_id}"
    )


@adoption_organization_pages_router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def update_adoption_organizations(
    adoption_organization: AdoptionOrganizations
):
    """

    Args:
        adoption_organization:

    Returns:

    """
    try:
        adoption_organization = adoption_organization.update()
        return adoption_organization

    except HTTPError as e:
        raise HTTPException(status_code=e.code, detail=e.reason)

    except Exception as e:
        raise HTTPException(status_code=424, detail=f"Could not update organization due to: {e}")


@adoption_organization_pages_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_adoption_organizations(
    adoption_organization_id: str
):
    """

    Args:
        adoption_organization_id:

    Returns:

    """
    try:
        DatabaseManager.delete_from_db(db_name=db_name, key=adoption_organization_id)

    except ValueError:
        return HTTPException(status_code=404, detail=f"Could not find adoption listing")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Could not delete adoption listing due to: {e}")
