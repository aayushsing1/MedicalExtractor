from fastapi import FastAPI, Form, UploadFile, File, Request
import uvicorn
from extractor import extract
import uuid
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.responses import FileResponse
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/home", response_class=HTMLResponse)
async def opens(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/help", response_class=HTMLResponse)
async def helps(request: Request):
    return templates.TemplateResponse("help.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def abouts(request: Request):
    return templates.TemplateResponse("aboutus.html", {"request": request})

@app.get("/downloadpdex")
async def download_file():
    return FileResponse("static/pd_1.pdf", filename="Ex--Patient_Details.pdf")

@app.get("/downloadpreex")
async def download_file():
    return FileResponse("static/pre_1.pdf", filename="Ex--Prescription.pdf")


@app.post("/extract_from_doc")
def extract_from_doc(
        file_format: str = Form(...),
        file: UploadFile = File(...),
):
    contents = file.file.read()

    file_path = "../uploads/" + str(uuid.uuid4()) + ".pdf"

    with open(file_path,"wb") as f:
        f.write(contents)

    try:
        data = extract(file_path, file_format)
    except Exception as e:
        data = {
            'error': str(e)
        }

    if os.path.exists(file_path):
        os.remove(file_path)

    return data

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)