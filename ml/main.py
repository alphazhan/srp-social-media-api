import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import detect_language, extract_hashtags, moderate_text
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="ML Inference Service", version="0.1.0")

# --- CORS Configuration ---
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

app.include_router(detect_language.router)
app.include_router(extract_hashtags.router)
app.include_router(moderate_text.router)


@app.on_event("startup")
async def load_models():
    print("Loading three models...")

    # These imports force preloading so they’re ready on first request
    from services.detect_language import _classifier
    from services.extract_hashtags import model
    from services.moderate_text import _model

    _classifier
    model
    _model

    print("Three models are loaded")


def main():
    print("Hello from ml!")


if __name__ == "__main__":
    main()
