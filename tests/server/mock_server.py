import io

import fastapi
import uvicorn
from fastapi import UploadFile, File

import tests

app = fastapi.FastAPI()


handler = '/raise'
@app.get(handler, status_code=200)
async def raise_method():
    raise fastapi.HTTPException(status_code=400)


handler = '/method'
@app.post(handler, status_code=200)
async def post_method():
    return {'success': True}


handler = '/method'
@app.get(handler, status_code=200)
async def get_method():
    return {'success': True}


handler = '/file:request'
@app.post(handler, status_code=200)
async def file_method(file: UploadFile = File(...),):
    return {'success': True}


handler = '/file:response'
@app.post(handler, status_code=200, response_model=None)
async def file_method_response(file: UploadFile = File(...),):
    return fastapi.responses.StreamingResponse(io.StringIO(str(await file.read())), media_type='text/plain')


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=tests.port)
