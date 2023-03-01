""" Base App Config """

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.authentication import AuthenticationBackend

from core.config import Settings
from apis import (
    adoption_pages_router,
    adoption_fetchers_pages_router,
    adoption_organization_pages_router,
    general_pages_router
)
# from auth import auth_app

ROUTERS_LIST = [
    general_pages_router,
    adoption_pages_router,
    adoption_fetchers_pages_router,
    adoption_organization_pages_router,
]


ALLOWED_HOSTS = ["*"]



######################################################

# class BearerTokenAuthBackend(AuthenticationBackend):
#     """
#     This is a custom auth backend class that will allow you to authenticate your request and return auth and user as
#     a tuple
#     """
#     async def authenticate(self, request):
#         # This function is inherited from the base class and called by some other class
#         if "Authorization" not in request.headers:
#             return
#
#         auth = request.headers["Authorization"]
#         try:
#             scheme, token = auth.split()
#             if scheme.lower() != 'bearer':
#                 return
#             decoded = jwt.decode(
#                 token,
#                 settings.JWT_SECRET,
#                 algorithms=[settings.JWT_ALGORITHM],
#                 options={"verify_aud": False},
#             )
#         except (ValueError, UnicodeDecodeError, JWTError) as exc:
#             raise AuthenticationError('Invalid JWT Token.')
#
#         username: str = decoded.get("sub")
#         token_data = TokenData(username=username)
#         # This is little hack rather making a generator function for get_db
#         db = LocalSession()
#         user = User.objects(db).filter(User.id == token_data.username).first()
#         # We must close the connection
#         db.close()
#         if user is None:
#             raise AuthenticationError('Invalid JWT Token.')
#         return auth, user

######################################################


def include_router(app_context):
    for router in ROUTERS_LIST:
        app_context.include_router(router=router)


def configure_static(app_context):
    app_context.mount("/static", StaticFiles(directory=f"static"), name="static")


def start_application():
    new_app = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)
    include_router(app_context=new_app)
    configure_static(app_context=new_app)
    # new_app.mount(app=auth_app, path="/auth")

    return new_app


app = start_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



################

import os
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth

# OAuth settings
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Set up oauth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)
from starlette.middleware.sessions import SessionMiddleware
SECRET_KEY = os.environ.get('SECRET_KEY') or None
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

################ Login routes
from fastapi import Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError

@app.route('/login')
async def login(request: Request):
    if os.environ.get("ENVIRONMENT") == "local":
        redirect_uri = request.url_for('auth')  # This creates the url for the /auth endpoint
    else:
        # TODO: need to figure out why this is misbehaving on deta
        redirect_uri = "https://ruffday.ca/auth"  # This creates the url for the /auth endpoint
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return RedirectResponse(url="/")
    user_data = access_token.get("userinfo")
    request.session['user'] = dict(user_data)
    return RedirectResponse(url='/')


@app.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')
