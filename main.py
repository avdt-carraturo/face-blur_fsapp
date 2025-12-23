from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from blur_faces import blur_faces
import tempfile
import shutil

app = FastAPI()

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
