from typing import Dict
from urllib.error import HTTPError
from models import AdoptionListings, AdoptionDetails
from models.shared import ListingTypes
from fastapi import HTTPException, status, APIRouter, Request
from utils import DatabaseManager
from core.config import Settings
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory=f"templates")
TEMPLATES_SUB = "adoptions_pages"
adoption_pages_router = APIRouter(
    prefix="/adoptions",
    tags=["adoptions"]
)


db_name = Settings.ADOPTIONS_DB_NAME


def get_adoption_listings_from_db(params: dict = None):
    query_params = {
        "listing_type": ListingTypes.ADOPTIONS.value
    }
    if params:
        query_params.update({"address": params})

    all_adoption_listings = DatabaseManager.search_db(
        db_name=db_name,
        search_params=query_params
    )
    adoption_listings = [AdoptionListings(**adoption_listing) for adoption_listing in all_adoption_listings.items]

    return adoption_listings


@adoption_pages_router.get("/")
async def home(request: Request):
    """

    Args:
        request:

    Returns:

    """
    adoption_listings = get_adoption_listings_from_db(params=request.query_params.get("searchValue"))
    return templates.TemplateResponse(f"{TEMPLATES_SUB}/adoptions.html", {"request": request, "adoptions": adoption_listings})


@adoption_pages_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_adoption_listingss(
    adoption_listing: AdoptionListings,
    adoption_details: AdoptionDetails = None,
):
    """
    An endpoint to create a new adoption detail
    Args:
        adoption_listing (dict): the Adoption Listing information
        adoption_details (dict): the Adoption Details information

    Returns:
        a json object with the details of the new listing on successful creation, else 424 error

    Raises:
        HTTPException 409 or 424 on failed creation
    """
    try:
        new_adoption_detail = adoption_details.save() if adoption_details else None
        adoption_listing.details_id = new_adoption_detail.key if new_adoption_detail else None
        new_adoption = adoption_listing.save()

        return new_adoption
    except HTTPError as e:
        raise HTTPException(status_code=e.code, detail=e.reason)

    except Exception as e:
        raise HTTPException(status_code=424, detail=f"Could not add listing due to: {e}")


@adoption_pages_router.post("/search", status_code=status.HTTP_200_OK)
async def get_all_adoption_listings(
    search_params: Dict = None
):
    """
    An Endpoint to search or get all listed adoption details
    Args:
        search_params: Name of the available adoption

    Returns:
         a json object of all available listings
    """

    query_params = {
        "listing_type": ListingTypes.ADOPTIONS.value
    }

    if search_params:
        query_params.update(search_params)

    all_adoptions = DatabaseManager.search_db(
        db_name=db_name,
        search_params=query_params
    )
    if all_adoptions.count:
        return all_adoptions.items
    else:
        return {"message": f"Nothing to see here..."}


@adoption_pages_router.get("/{adoption_id}", status_code=status.HTTP_200_OK)
async def get_adoption_listings(adoption_id: str):
    """
    An endpoint to get the adoption details of a single listing
    Args:
        adoption_id (str): The unique ID of a listing

    Returns:
        a json object with the details of the adoption listing

    """
    adoption_details = DatabaseManager.read_from_db(
        db_name=db_name,
        key=adoption_id)
    return adoption_details if adoption_details else HTTPException(status_code=404, detail=f"No listing found for {adoption_id}")


@adoption_pages_router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def update_adoption_listings(
    adoption_listing: AdoptionListings,
    adoption_detail: AdoptionDetails
):
    """
    An endpoint to update an adoption detail
    Args:
        adoption_listing (dict): a Dict containing the details of a new adoption listing
        adoption_detail (dict):

    Returns:
        a json object with the details of the new listing on successful creation, else 424 error

    Raises:
        HTTPException 409 or 424 on failed creation
    """
    try:
        adoption_listing = adoption_listing.update()
        adoption_detail = adoption_detail.update()
        return {"adoption_listing": adoption_listing, "adoption_detail": adoption_detail}

    except HTTPError as e:
        raise HTTPException(status_code=e.code, detail=e.reason)

    except Exception as e:
        raise HTTPException(status_code=424, detail=f"Could not update listing due to: {e}")


@adoption_pages_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_adoption_listings(adoption_id: str):
    """
    Endpoint to delete an existing adoption detail
    Args:
        adoption_id (str): adoption ID of the adoption listing to delete

    Returns:
        200 on successful delete

    Raises:
        HTTPException on failed delete
    """
    try:
        DatabaseManager.delete_from_db(db_name=db_name, key=adoption_id)

    except ValueError:
        return HTTPException(status_code=404, detail=f"Could not find adoption listing")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Could not delete adoption listing due to: {e}")
