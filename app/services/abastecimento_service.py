from decimal import Decimal
from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.abastecimento import Abastecimento, TipoCombustivel
from app.schemas.abastecimento import AbastecimentoCreate, HistoricoResponse 
from app.repositories.abastecimento_repository import AbastecimentoRepository


LIMIAR_ANOMALIA = Decimal("1.25")  # +25%


class AbastecimentoService:
    """Serviço de domínio para regras de abastecimento."""

    def __init__(self, session: AsyncSession):
        self.repository = AbastecimentoRepository(session)

    async def create_abastecimento(
        self, data: AbastecimentoCreate
    ) -> Abastecimento:
        """
        Cria um abastecimento aplicando a regra de anomalia.
        """
        media_historica = await self.repository.get_media_preco_por_combustivel(
            data.tipo_combustivel
        )

        improper_data = False

        if media_historica is not None:
            if data.preco_por_litro > media_historica * LIMIAR_ANOMALIA:
                improper_data = True

        abastecimento = Abastecimento(
            id_posto=data.id_posto,
            data_hora=data.data_hora,
            tipo_combustivel=data.tipo_combustivel,
            preco_por_litro=data.preco_por_litro,
            volume_abastecido=data.volume_abastecido,
            cpf_motorista=data.cpf_motorista,
            improper_data=improper_data,
        )

        return await self.repository.create(abastecimento)

    async def get_historico_motorista(self, cpf_motorista: str) -> HistoricoResponse:
        """
        Retorna o histórico de abastecimentos de um motorista (CPF).
        """
        abastecimentos = await self.repository.get_by_cpf(cpf_motorista)

        return HistoricoResponse(
            cpf_motorista=cpf_motorista,
            total_abastecimentos=len(abastecimentos),
            abastecimentos=abastecimentos,
        )
    
    async def list_abastecimentos(
        self,
        page: int,
        size: int,
        tipo_combustivel: Optional[TipoCombustivel],
        data_inicio: Optional[datetime],
        data_fim: Optional[datetime],
    ) -> Tuple[List[Abastecimento], int]:
        """
        Retorna uma lista paginada de abastecimentos com filtros opcionais.
        """
        return await self.repository.get_all(
            page=page,
            size=size,
            tipo_combustivel=tipo_combustivel,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )

    