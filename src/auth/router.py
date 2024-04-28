from fastapi import APIRouter

from src.auth.config import RouterConfig


router = APIRouter(
    prefix=RouterConfig.PREFIX,
    tags=RouterConfig.tags_list(),
)
