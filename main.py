from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import tempfile
import os
from blur_faces import blur_faces

app = FastAPI()

@app.post("/blur")
async def blur(file: UploadFile = File(...)):
    # Estensione reale del file
    suffix = os.path.splitext(file.filename)[1].lower() or ".tmp"

    # File temporanei unici
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as input_file:
        input_path = input_file.name
        input_file.write(await file.read())

    output_path = input_path + "_blurred"

    try:
        blur_faces(input_path, output_path)
        return FileResponse(output_path)
    finally:
        # Pulizia file temporanei
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
