"""SESS single-deployable web application entry point."""

from fastapi import FastAPI
from app.web_interface import router

app = FastAPI(
    title="SESS",
    version="0.1.0",
    description="Runnable API skeleton. Business operations are intentionally unimplemented.",
)

app.include_router(router)


@app.get("/")
async def health_check() -> dict[str, str]:
    return {"application": "SESS", "status": "skeleton"}
