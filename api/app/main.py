from typing import Any

from fastapi import FastAPI
from fastapi.responses import FileResponse

# from fastapi.staticfiles import StaticFiles
from app.routers import router

FAVICON_PATH = "app/favicon.ico"

app = FastAPI(
    title="Fox Adventure app",
    description="""
        Simple app for getting list of cruise ships data for Akureyri
        ports and tracking data updates to adjust passengers lists on
        booking systems.
        """,
)

app.include_router(router)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> Any:
    return FileResponse(FAVICON_PATH)


# app.mount("/static", StaticFiles(directory="static"), name="static")

# DEBUGGING
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8001)
