from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.abastecimento import AbastecimentoCreate, AbastecimentoResponse
from app.services.abastecimento_service import AbastecimentoService

router = APIRouter(prefix="/api/v1/abastecimentos", tags=["Abastecimentos"])


@router.post(
    "",
    response_model=AbastecimentoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_abastecimento(   #async
    data: AbastecimentoCreate,
    db: AsyncSession = Depends(get_db),  #AsyncSession
):
    service = AbastecimentoService(db)
    return await service.create_abastecimento(data)  #await

