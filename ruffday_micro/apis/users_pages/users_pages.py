# from typing import Dict
# from urllib.error import HTTPError
# from models import AdoptionListings, AdoptionDetails
# from models.shared import ListingTypes
# from fastapi import HTTPException, status, APIRouter, Request
# from starlette.responses import RedirectResponse
# from authlib.integrations.starlette_client import OAuthError
# from utils import DatabaseManager
# from core.config import Settings
# from fastapi.templating import Jinja2Templates
#
#
# templates = Jinja2Templates(directory=f"templates")
# TEMPLATES_SUB = "users_pages"
# adoption_pages_router = APIRouter(
#     prefix="/users",
#     tags=["users"]
# )
#
# db_name = Settings.USERS_DB_NAME
#
#
# @adoption_pages_router.get("/login")
# async def login(request: Request):
#     redirect_uri = request.url_for('auth')  # This creates the url for the /auth endpoint
#     return await oauth.google.authorize_redirect(request, redirect_uri)
#
#
# @app.route('/auth')
# async def auth(request: Request):
#     try:
#         access_token = await oauth.google.authorize_access_token(request)
#     except OAuthError:
#         return RedirectResponse(url='/')
#     user_data = await oauth.google.parse_id_token(request, access_token)
#     request.session['user'] = dict(user_data)
#     return RedirectResponse(url='/')
