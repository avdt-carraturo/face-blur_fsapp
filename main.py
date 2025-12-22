from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from blur_faces import blur_faces

app = FastAPI()

@app.post("/blur")
async def blur(request: Request):
    input_path = "/tmp/input"
    output_path = "/tmp/output"

    with open(input_path, "wb") as f:
        f.write(await request.body())

    blur_faces(input_path, output_path)

    return FileResponse(output_path)
