import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from .api import health, jewelry, results, tryon
from .websocket import tryon_socket
from .core.config import settings
from .core.errors import AppError, fail

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def create_app() -> FastAPI:
    app = FastAPI(title="Virtual Jewellery Try-On API")
    app.add_middleware(CORSMiddleware, allow_origins=list(settings.origins),
                       allow_methods=["*"], allow_headers=["*"])

    @app.exception_handler(AppError)
    async def _app_err(_: Request, e: AppError):
        return JSONResponse(fail(e.code, e.message), status_code=e.status)

    @app.exception_handler(RequestValidationError)
    async def _val_err(_: Request, e: RequestValidationError):
        return JSONResponse(fail("INVALID_REQUEST", "Missing or invalid request fields."), status_code=422)

    @app.exception_handler(Exception)
    async def _any_err(_: Request, e: Exception):
        logging.getLogger("app").exception("unhandled error")
        return JSONResponse(fail("PROCESSING_FAILED", "Something went wrong while processing."), status_code=500)

    for r in (health, jewelry, tryon, results):
        app.include_router(r.router, prefix="/api")
    app.include_router(tryon_socket.router)
    app.mount("/assets", StaticFiles(directory=settings.assets_dir), name="assets")
    app.mount("/outputs", StaticFiles(directory=settings.outputs_dir), name="outputs")
    return app


app = create_app()
