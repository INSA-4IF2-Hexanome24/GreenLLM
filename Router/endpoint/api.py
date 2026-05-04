import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from service.carbon_computing import calculate_request_carbon_footprint


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
def calculate_request_carbon_footprint_endpoint() -> JSONResponse:
    """Return the mock carbon footprint payload as JSON."""
    return JSONResponse(content=calculate_request_carbon_footprint())


@main.get("/bestLLM")
def get_best_llm() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:main", host="127.0.0.1", port=8000, reload=True)