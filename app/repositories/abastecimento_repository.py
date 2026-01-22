from typing import Sequence
from decimal import Decimal

from sqlalchemy import select
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
