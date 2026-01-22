from fastapi import APIRouter, Depends, status , HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models.abastecimento import TipoCombustivel
from app.schemas.abastecimento import (AbastecimentoCreate, AbastecimentoResponse,
HistoricoResponse , AbastecimentoPagination)
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


@router.get("/motoristas/{cpf}/historico", response_model=HistoricoResponse)
async def historico_motorista(
    cpf: str,
    db: AsyncSession = Depends(get_db),
):
    if len(cpf) != 11 or not cpf.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF inválido",
        )

    service = AbastecimentoService(db)
    historico = await service.get_historico_motorista(cpf)

    if historico.total_abastecimentos == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum abastecimento encontrado",
        )

    return historico


@router.get("", response_model=AbastecimentoPagination)
async def list_abastecimentos(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    tipo_combustivel: Optional[TipoCombustivel] = Query(None),
    data_inicio: Optional[datetime] = Query(None),
    data_fim: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    service = AbastecimentoService(db)
    items, total = await service.list_abastecimentos(
        page=page,
        size=size,
        tipo_combustivel=tipo_combustivel,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size,
    }