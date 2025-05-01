from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import verify
from services.logic import start_subscribers


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

    @app.get("/")
    def root():
        return {"message": "RENTit Pi Backend API is running"}

    return app


app = create_app()

start_subscribers()
