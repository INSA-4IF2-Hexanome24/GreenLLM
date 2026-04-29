import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


DEFAULT_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]


def get_cors_origins() -> list[str]:
    raw_origins = os.getenv("LLMROUTER_CORS_ORIGINS", "").strip()
    if raw_origins:
        origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
        if origins:
            return origins
    return DEFAULT_CORS_ORIGINS


main = FastAPI(title="LLMRouter API", version="0.1.0")
app = main

main.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@main.get("/")
def root() -> dict[str, str]:
    return {"message": "LLMRouter API is running. See available endpoints at /docs."}


@main.get("/carbon")
def calculate_request_carbon_footprint() -> dict[str, str]:
    return {"status": "ok"}


@main.get("/bestLLM")
def get_best_llm() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:main", host="127.0.0.1", port=8000, reload=True)