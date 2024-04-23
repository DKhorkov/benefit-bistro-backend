import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request,
        # context={"title": "Benefit Bistro"},
    )


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", default=8080), log_level="info", reload=True)
