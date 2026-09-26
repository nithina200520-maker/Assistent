import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response

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

    def read_file_content(filename: str) -> str:
        candidates = [
            os.path.join(base_dir, filename),
            os.path.join(static_dir, filename),
            os.path.join(base_dir, "frontend", filename),
        ]
        for path in candidates:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        return f.read()
                except Exception:
                    pass
        return ""

    @app.get("/", response_class=HTMLResponse)
    @app.get("/api/index", response_class=HTMLResponse)
    @app.get("/api/index.py", response_class=HTMLResponse)
    async def serve_index():
        html = read_file_content("index.html")
        if html:
            return HTMLResponse(content=html)
        return HTMLResponse(content="<h1>AegisRecover AI Platform</h1><p>Server running cleanly.</p>")

    @app.get("/app.js")
    @app.get("/api/app.js")
    async def serve_js():
        js = read_file_content("app.js")
        return Response(content=js, media_type="application/javascript")

    @app.get("/style.css")
    @app.get("/api/style.css")
    async def serve_css():
        css = read_file_content("style.css")
        return Response(content=css, media_type="text/css")

    return app

app = create_app()
