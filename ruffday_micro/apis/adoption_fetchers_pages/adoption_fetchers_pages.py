from fastapi import HTTPException, status, APIRouter, Request
from fastapi.templating import Jinja2Templates
from bs4 import BeautifulSoup


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


class HtmlAdoptionFetcher(BeautifulSoup):
    """
    Abstracts away the HTML parsing libraries used in the background.
    """

    def __init__(self, markup):
        """
        Simplified constructor that defaults BeautifulSoup to using the
         built-in Python HTML parsing libraries.

        Args:
            markup:  A string or a file-like object representing markup
              to be parsed.
        """
        super().__init__(markup, 'html.parser')

    def find_adoptions(self):
        raise NotImplementedError


class TorontoHumaneSocietyFetcher(HtmlAdoptionFetcher):
    """
    Fetcher that parses dogs available for adoption from the Toronto Humane
      Society. The URL is stored in TorontoHumaneSocietyFetcher.ADOPTIONS_URL.
    """

    ADOPTIONS_URL = 'https://www.torontohumanesociety.com/adoption-and-rehoming/adopt/dog-adopt-process/'

    def find_names(self):
        """
        Finds the names for all the pets listed on the page.
         Does not check for availability of the pet.
        
        Returns:
             a list of strings, where each item is the name of a different pet
        """
        names_divs = self.find_all('div', 'title')
        names_h2s = [div.find('h2') for div in names_divs]
        names = [h2.string if h2 else '' for h2 in names_h2s]
        return names

    def find_adoptions(self):
        return self.find_all('div', 'title')
