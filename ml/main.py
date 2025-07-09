from fastapi import FastAPI
from ml.routers import detect_language, extract_hashtags, moderate_text

app = FastAPI(
    title="ML Inference Service",
    version="0.1.0"
)

app.include_router(detect_language.router)
app.include_router(extract_hashtags.router)
app.include_router(moderate_text.router)

def main():
    print("Hello from ml!")


if __name__ == "__main__":
    main()
