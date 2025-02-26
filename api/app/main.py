from fastapi import FastAPI

# from fastapi.staticfiles import StaticFiles
from app.routers import router

app = FastAPI(
    title="Fox Adventure app",
    description="""
        Simple app for getting list of cruise ships data for Akureyri
        ports and tracking data updates to adjust passengers lists on
        booking systems.
        """,
)

app.include_router(router)

# app.mount("/static", StaticFiles(directory="static"), name="static")

# DEBUGGING
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8001)
