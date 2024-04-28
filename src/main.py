import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from src.config import PathsConfig, cors_config, PageNamesConfig, uvicorn_config


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.ALLOW_ORIGINS,
    allow_credentials=cors_config.ALLOW_CREDENTIALS,
    allow_methods=cors_config.ALLOW_METHODS,
    allow_headers=cors_config.ALLOW_HEADERS,
)

app.mount('/static', StaticFiles(directory=PathsConfig.STATIC), name='static')

templates = Jinja2Templates(directory=PathsConfig.TEMPLATES.__str__())


@app.get('/', response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse(
        name=PathsConfig.INDEX_PAGE.__str__(),
        request=request,
        context={'title': PageNamesConfig.INDEX_PAGE},
    )


if __name__ == '__main__':
    uvicorn.run(
        'src.main:app',
        host=uvicorn_config.HOST,
        port=uvicorn_config.PORT,
        log_level=uvicorn_config.LOG_LEVEL,
        reload=uvicorn_config.RELOAD
    )
