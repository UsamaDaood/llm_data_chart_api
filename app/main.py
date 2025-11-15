from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.health import router as health_router
from app.routers.datasets import router as datasets_router
from app.routers.charts import router as charts_router

app = FastAPI(
    title="LLM Data-to-Chart API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(datasets_router, prefix="/datasets", tags=["datasets"])
app.include_router(charts_router, prefix="/charts", tags=["charts"])
