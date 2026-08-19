"""FastAPI Server for AuditVector."""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routes.audits import router as audits_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="AuditVector API",
        description="Autonomous Financial Integrity & Evidence-Backed Audit Engine",
        version="1.0.0"
    )

    # Enable CORS for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health")
    def health_check():
        return {"status": "HEALTHY", "system": "AuditVector", "version": "1.0.0"}

    # Include API routes
    app.include_router(audits_router)

    # Mount static frontend directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    frontend_dir = os.path.join(base_dir, "frontend")

    if os.path.exists(frontend_dir):
        app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

        @app.get("/")
        def serve_index():
            return FileResponse(os.path.join(frontend_dir, "index.html"))

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.api.server:app", host="0.0.0.0", port=8000, reload=True)
