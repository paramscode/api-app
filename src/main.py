from fastapi import FastAPI
from src.api.endpoints import csv, health

app = FastAPI(title="Data Backend API", version="1.0.0")

app.include_router(csv.router)
app.include_router(health.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)