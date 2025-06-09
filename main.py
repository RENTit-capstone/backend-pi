from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import verify, gpio, system
from services.logic import start_subscribers
import os


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    

    app.include_router(verify.router, prefix="/api")
    app.include_router(gpio.router, prefix="/api")
    app.include_router(system.router, prefix="/api")

    app.mount("/styles", StaticFiles(directory=os.path.join("static", "styles")), name="styles")
    app.mount("/src", StaticFiles(directory=os.path.join("static", "src")), name="src")
    app.mount("/", StaticFiles(directory=os.path.join("static", "public"), html=True), name="static")

    return app


app = create_app()

start_subscribers()
