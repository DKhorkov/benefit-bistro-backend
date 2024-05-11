from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse, Response, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from src.auth.models import UserModel
from src.auth.config import RouterConfig, URLPathsConfig, PageNamesConfig, URLNamesConfig, PathsConfig, cookies_config
from src.celery.tasks.auth_tasks import send_verify_email_message
from src.core.utils import generate_html_context
from src.security.models import JWTDataModel
from src.security.utils import create_jwt_token
from src.auth.dependencies import (
    login_user,
    register_user,
    authenticate_user,
    verify_user_email
)


router = APIRouter(
    prefix=RouterConfig.PREFIX,
    tags=RouterConfig.tags_list(),
)

# Mounts:
templates = Jinja2Templates(directory=PathsConfig.TEMPLATES.__str__())


@router.get(path=URLPathsConfig.REGISTER_PAGE, response_class=HTMLResponse, name=URLNamesConfig.REGISTER_PAGE)
async def register_page(request: Request):
    return templates.TemplateResponse(
        name=PathsConfig.REGISTER_PAGE.__str__(),
        request=request,
        context=generate_html_context(
            title=PageNamesConfig.REGISTER_PAGE
        )
    )


@router.get(path=URLPathsConfig.LOGIN_PAGE, response_class=HTMLResponse, name=URLNamesConfig.LOGIN_PAGE)
async def login_page(request: Request):
    return templates.TemplateResponse(
        name=PathsConfig.LOGIN_PAGE.__str__(),
        request=request,
        context=generate_html_context(
            title=PageNamesConfig.LOGIN_PAGE
        )
    )


@router.post(path=URLPathsConfig.REGISTER, response_class=RedirectResponse, name=URLNamesConfig.REGISTER)
async def register(user: UserModel = Depends(register_user)):
    send_verify_email_message.delay(user_data=await user.to_dict())
    return RedirectResponse(
        url=router.prefix + URLPathsConfig.LOGIN_PAGE,
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get(path=URLPathsConfig.VERIFY_EMAIL, response_class=RedirectResponse, name=URLNamesConfig.VERIFY_EMAIL)
async def verify_email(token: str):
    await verify_user_email(token=token)
    return RedirectResponse(
        url=router.prefix + URLPathsConfig.EMAIL_VERIFIED,
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get(path=URLPathsConfig.EMAIL_VERIFIED, response_class=HTMLResponse, name=URLNamesConfig.EMAIL_VERIFIED)
async def email_verified_page(request: Request):
    return templates.TemplateResponse(
        name=PathsConfig.EMAIL_VERIFIED.__str__(),
        request=request,
        context=generate_html_context(
            title=PageNamesConfig.EMAIL_VERIFIED
        )
    )


@router.post(path=URLPathsConfig.LOGIN, response_class=Response, name=URLNamesConfig.LOGIN)
async def login(user: UserModel = Depends(login_user)):
    jwt_data: JWTDataModel = JWTDataModel(user_id=user.id)
    token: str = await create_jwt_token(jwt_data=jwt_data)
    response: Response = Response()
    response.set_cookie(
        key=cookies_config.COOKIES_KEY,
        value=token,
        secure=cookies_config.SECURE_COOKIES,
        httponly=cookies_config.HTTP_ONLY,
        expires=datetime.now(tz=timezone.utc) + timedelta(days=cookies_config.COOKIES_LIFESPAN_DAYS),
        samesite=cookies_config.SAME_SITE
    )
    return response


@router.get(path=URLPathsConfig.LOGOUT, response_class=Response, name=URLNamesConfig.LOGOUT)
async def logout():
    response: Response = Response()
    response.delete_cookie(
        key=cookies_config.COOKIES_KEY,
        secure=cookies_config.SECURE_COOKIES,
        httponly=cookies_config.HTTP_ONLY,
        samesite=cookies_config.SAME_SITE
    )
    return response


@router.get(path=URLPathsConfig.ME, response_class=JSONResponse, response_model=UserModel, name=URLNamesConfig.ME)
async def get_my_account(user: UserModel = Depends(authenticate_user)):
    return user
