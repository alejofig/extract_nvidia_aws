from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
import os
import shutil

app = FastAPI()

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Configura la carpeta de plantillas y archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_FOLDER}/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # Llamar a nv-ingest para procesar el archivo
        nv_ingest_command = [
            "nv-ingest",  # Asegúrate de que nv-ingest esté en el PATH
            "--input", file_location,
            "--output", f"{PROCESSED_FOLDER}/{file.filename}"
        ]
        subprocess.run(nv_ingest_command, check=True)

        # Leer el resultado procesado
        processed_file = f"{PROCESSED_FOLDER}/{file.filename}"
        with open(processed_file, "r") as result_file:
            result_data = result_file.read()

        return JSONResponse(content={"result": result_data})
    except subprocess.CalledProcessError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        # Limpieza de archivos temporales
        os.remove(file_location)
        os.remove(f"{PROCESSED_FOLDER}/{file.filename}")
