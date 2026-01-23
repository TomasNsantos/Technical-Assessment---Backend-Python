from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    response_description="Status da API e seus componentes",
)
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Verifica saúde da API e conectividade com banco de dados.
    
    Retorna:
    - status: Estado geral (healthy/degraded)
    - version: Versão da aplicação
    - timestamp: Momento da verificação (UTC)
    - services: Status de cada serviço
    """
    db_status = "healthy"
    
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "version": settings.api_version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": {
            "database": db_status,
        },
    }