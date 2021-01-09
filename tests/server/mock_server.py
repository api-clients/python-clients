import io
from typing import List, Optional

import fastapi
import uvicorn
from fastapi import UploadFile, File, Form
from loguru import logger

import tests
from pydantic import BaseModel


app = fastapi.FastAPI()


handler = '/raise'
@app.get(handler, status_code=200)
async def raise_method():
    logger.debug(f"")
    raise fastapi.HTTPException(status_code=400)


handler = '/method'
@app.post(handler, status_code=200)
async def post_method():
    logger.debug(f"")
    return {'success': True}


handler = '/method'
@app.get(handler, status_code=200)
async def get_method():
    logger.debug(f"")
    return {'success': True}


handler = '/file:request'
@app.post(handler, status_code=200)
async def file_method(file: UploadFile = File(...),):
    logger.debug(f"")
    return {'success': True}


handler = '/manyfiles'
@app.post(handler, status_code=200)
async def files_method(files: List[UploadFile] = File(...),):
    logger.debug(f"")
    if len(files) != 3:
        raise fastapi.HTTPException(status_code=400)
    return {'success': True}


handler = '/manyfilesanddata'
@app.post(handler, status_code=200)
async def files_method(files: List[UploadFile] = File(...), data1: str = Form(...), data2: Optional[int] = Form(None)):
    logger.debug(f"")
    if len(files) != 3:
        raise fastapi.HTTPException(status_code=400)
    if data1 != "data1":
        raise fastapi.HTTPException(status_code=400)
    if data2 != 12345:
        raise fastapi.HTTPException(status_code=400)
    return {'success': True}


class Item(BaseModel):
    data1: str
    data2: int
    data3: bool

handler = '/datadict'
@app.post(handler, status_code=200)
async def datadict_method(item: Item):
    logger.debug(f"item {item}")
    if item.data1 != "data1":
        raise fastapi.HTTPException(status_code=400)
    if item.data2 != 12345:
        raise fastapi.HTTPException(status_code=400)
    if item.data3:
        raise fastapi.HTTPException(status_code=400)
    return {'success': True}


handler = '/file:response'
@app.post(handler, status_code=200, response_model=None)
async def file_method_response(file: UploadFile = File(...),):
    logger.debug(f"")
    b = (await file.read()).decode()
    return fastapi.responses.StreamingResponse(io.StringIO(b), media_type='text/plain')


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=tests.server_port)
