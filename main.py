from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services import Converter

app = FastAPI()


app.mount("/static", StaticFiles(directory="static", check_dir=True), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request):
    return templates.TemplateResponse(request=request, name="homepage.html")


@app.post("/convert")
async def convert_image(
    request: Request, size: int = Form(...), image: UploadFile = File(...)
):
    print(size)
    _service = Converter(image, size)
    value = _service.convert()
    return templates.TemplateResponse(
        request=request, name="result.html", context={"result": value}
    )
