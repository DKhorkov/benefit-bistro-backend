from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from src.config import PathsConfig, cors_config, PageNamesConfig, URLPathsConfig, URLNamesConfig
from src.auth.router import router as auth_router
from src.core.database.orm import start_mappers
from src.core.utils import generate_html_context


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    """
    Runs events before application startup and after application shutdown.
    """

    # Startup events:
    start_mappers()

    yield

    # Shutdown events:

app = FastAPI(lifespan=lifespan)

# Middlewares:
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.ALLOW_ORIGINS,
    allow_credentials=cors_config.ALLOW_CREDENTIALS,
    allow_methods=cors_config.ALLOW_METHODS,
    allow_headers=cors_config.ALLOW_HEADERS,
)

# Routers:
app.include_router(auth_router)

# Mounts:
app.mount(path=URLPathsConfig.STATIC, app=StaticFiles(directory=PathsConfig.STATIC), name=URLNamesConfig.STATIC)
templates = Jinja2Templates(directory=PathsConfig.TEMPLATES.__str__())


@app.get(path=URLPathsConfig.HOMEPAGE, response_class=HTMLResponse, name=URLNamesConfig.HOMEPAGE)
async def homepage(request: Request):
    return templates.TemplateResponse(
        name=PathsConfig.HOMEPAGE.__str__(),
        request=request,
        context=generate_html_context(
            title=PageNamesConfig.HOMEPAGE
        )
    )
