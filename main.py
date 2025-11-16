from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse
import uuid, os

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def home():
    html_content = """
    <html>
        <body>
            <h2>File Upload</h2>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    download_link = f"https://YOUR-RENDER-URL/download/{file_id}"
    return {"status":"success","link":download_link}

@app.get("/download/{file_id}")
async def download(file_id: str):
    for filename in os.listdir(UPLOAD_DIR):
        if filename.startswith(file_id):
            return FileResponse(f"{UPLOAD_DIR}/{filename}")
    return {"error":"File not found"}
