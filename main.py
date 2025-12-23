from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from blur_faces import blur_faces
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import shutil

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://travelwithsecurity.netlify.app",  # Flutter web deployato
        "http://localhost",
        "http://localhost:*",
        "http://127.0.0.1",
        "http://127.0.0.1:*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/blur")
async def blur(file: UploadFile = File(...)):
    ext = "." + file.filename.split(".")[-1]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as in_tmp:
        input_path = in_tmp.name
        shutil.copyfileobj(file.file, in_tmp)

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as out_tmp:
        output_path = out_tmp.name

    blur_faces(input_path, output_path)

    return FileResponse(output_path, media_type="image/jpeg")
