import zlib
import logging
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
import api

app = FastAPI()

app.include_router(api.router)

logging.basicConfig(level=logging.INFO)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request({request.method}) {request.url}")
    response: StreamingResponse = await call_next(request)
    logging.info(f"Response: status_code={response.status_code}")

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    response.headers["X-CRC32"] = str(zlib.crc32(response_body))

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )


@app.get("/ping")
async def ping():
    return {"message": "pong"}
