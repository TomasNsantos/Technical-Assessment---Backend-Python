from fastapi import FastAPI
from app.config import settings
from app.api.routers import abastecimento, health


app = FastAPI(
    title="V-Lab Transport API",
    description="API de Ingestão de Dados de Abastecimento",
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(abastecimento.router)
app.include_router(health.router)
