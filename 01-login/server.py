#prompt to start server-> "unicorv server_fast:app"
#!pip install fastapi uvicorn python-dotenv authlib starlette
#!pip install "fastapi[standard]"

import os
from urllib.parse import urlencode, quote_plus #montam URLs com parâmetros

from fastapi import FastAPI, Request #requisição HTTP
from fastapi.responses import HTMLResponse, RedirectResponse #respostas HTTP
from starlette.middleware.sessions import SessionMiddleware #gerencia sessões de usuário
from authlib.integrations.starlette_client import OAuth #integração do Authlib com Starlette para autenticação OAuth
from dotenv import load_dotenv #carrega variáveis de ambiente de um arquivo .env
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key=os.getenv("APP_SECRET_KEY"))

#configuração do OAuth
oauth = OAuth()
oauth.register(
    name="auth0",
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

# Rota principal que exibe a página inicial
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = request.session.get("user")
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "session": user,
            "pretty": user,
        }
    )

#página de autenticação do Auth0
@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("callback")
    return await oauth.auth0.authorize_redirect(request, redirect_uri)

# callback pra resposta do Auth0 apos o login
@app.get("/callback")
async def callback(request: Request):
    token = await oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return RedirectResponse(url="http://127.0.0.1:8050/")

# logout que redireciona para o Auth0
@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(
        url="https://"
        + os.getenv("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": str(request.url_for("home")),
                "client_id": os.getenv("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )
