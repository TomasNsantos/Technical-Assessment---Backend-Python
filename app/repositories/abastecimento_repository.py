from typing import List, Optional, Sequence, Tuple
from decimal import Decimal
from datetime import datetime

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.abastecimento import Abastecimento, TipoCombustivel


class AbastecimentoRepository:
    """Camada de acesso a dados para Abastecimento."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, abastecimento: Abastecimento) -> Abastecimento:
        self.session.add(abastecimento)
        await self.session.commit()
        await self.session.refresh(abastecimento)
        return abastecimento

    async def get_media_preco_por_combustivel(
        self, tipo_combustivel: TipoCombustivel
    ) -> Decimal | None:
        """
        Retorna a média histórica de preço por combustível.
        (Implementação mockada para o desafio.)
        """
        medias_mockadas = {
            TipoCombustivel.GASOLINA: Decimal("5.00"),
            TipoCombustivel.ETANOL: Decimal("3.50"),
            TipoCombustivel.DIESEL: Decimal("4.80"),
        }

        return medias_mockadas.get(tipo_combustivel)
    
    async def get_all(
        self,
        page: int,
        size: int,
        tipo_combustivel: Optional[TipoCombustivel],
        data_inicio: Optional[datetime],
        data_fim: Optional[datetime],
    ) -> Tuple[List[Abastecimento], int]:

        query = select(Abastecimento)
        count_query = select(func.count(Abastecimento.id))

        filters = []

        if tipo_combustivel:
            filters.append(Abastecimento.tipo_combustivel == tipo_combustivel)
        if data_inicio:
            filters.append(Abastecimento.data_hora >= data_inicio)
        if data_fim:
            filters.append(Abastecimento.data_hora <= data_fim)

        if filters:
            query = query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))

        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        offset = (page - 1) * size
        query = (
            query
            .order_by(Abastecimento.data_hora.desc())
            .offset(offset)
            .limit(size)
        )

        result = await self.session.execute(query)
        items = result.scalars().all()

        return list(items), total
    
    async def get_by_cpf(self, cpf: str) -> List[Abastecimento]:
        """
        Retorna todos os abastecimentos feitos por um motorista (CPF).
        """
        result = await self.session.execute(
            select(Abastecimento).where(Abastecimento.cpf_motorista == cpf)
            .order_by(Abastecimento.data_hora.desc())
        )
        return result.scalars().all()
