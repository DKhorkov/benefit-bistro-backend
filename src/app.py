from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import clear_mappers
from starlette import status

from src.config import PathsConfig, cors_config, URLPathsConfig, URLNamesConfig
from src.users.entrypoints.router import router as users_router
from src.groups.entypoints.router import router as groups_router
from src.users.adapters.orm import start_mappers as start_users_mappers
from src.groups.adapters.orm import start_mappers as start_groups_mappers


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    """
    Runs events before application startup and after application shutdown.
    """

    # Startup events:
    start_users_mappers()
    start_groups_mappers()

    yield

    # Shutdown events:
    clear_mappers()

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
app.include_router(users_router)
app.include_router(groups_router)

# Mounts:
app.mount(path=URLPathsConfig.STATIC, app=StaticFiles(directory=PathsConfig.STATIC), name=URLNamesConfig.STATIC)
templates = Jinja2Templates(directory=PathsConfig.TEMPLATES.__str__())


@app.get(
    path=URLPathsConfig.HOMEPAGE,
    response_class=RedirectResponse,
    name=URLNamesConfig.HOMEPAGE,
    status_code=status.HTTP_303_SEE_OTHER
)
async def homepage():
    return RedirectResponse(
        status_code=status.HTTP_303_SEE_OTHER,
        url=URLPathsConfig.DOCS
    )
