import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .routes import router

def create_app() -> FastAPI:
    app = FastAPI(
        title="AegisRecover AI - Forensic Data Recovery Platform",
        description="Next-generation AI-assisted data recovery, carving, reconstruction, and fragment correlation engine.",
        version="2.4.0"
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(router)

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")

    @app.get("/")
    async def serve_index():
        candidates = [
            os.path.join(base_dir, "index.html"),
            os.path.join(static_dir, "index.html"),
            os.path.join(base_dir, "frontend", "index.html"),
        ]
        for path in candidates:
            if os.path.exists(path):
                return FileResponse(path)
        return {"message": "AegisRecover AI Backend Running."}

    @app.get("/app.js")
    async def serve_js():
        candidates = [
            os.path.join(base_dir, "app.js"),
            os.path.join(static_dir, "app.js"),
            os.path.join(base_dir, "frontend", "app.js"),
        ]
        for path in candidates:
            if os.path.exists(path):
                return FileResponse(path)
        return {"error": "app.js not found"}

    @app.get("/style.css")
    async def serve_css():
        candidates = [
            os.path.join(base_dir, "style.css"),
            os.path.join(static_dir, "style.css"),
            os.path.join(base_dir, "frontend", "style.css"),
        ]
        for path in candidates:
            if os.path.exists(path):
                return FileResponse(path)
        return {"error": "style.css not found"}

    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    return app

app = create_app()
