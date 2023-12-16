from fastapi import FastAPI, status, File ,Response, UploadFile
from app.model.infer import model_infer
import json

app = FastAPI()

@app.post('/invocations')
async def invocations(file: UploadFile =  File(...)):

    img_binary = model_infer(await file.read())
    
    body = {
        "image_bytes": f"{img_binary}"
    }

    print("encoded image", body)

    return Response(json.dumps(body), media_type="application/json")

@app.get('/ping')
async def ping():
    return Response(
        status_code=status.HTTP_200_OK,
        media_type="text/plain",
    )
