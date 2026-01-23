import pytest
from decimal import Decimal
from datetime import datetime, timezone

from app.services.abastecimento_service import AbastecimentoService
from app.schemas.abastecimento import AbastecimentoCreate
from app.models.abastecimento import TipoCombustivel


class FakeRepository:
    """Fake simples para simular o repositório."""

    def __init__(self, media):
        self.media = media

    async def get_media_preco_por_combustivel(self, tipo):
        return self.media

    async def create(self, abastecimento):
        return abastecimento


@pytest.mark.asyncio
async def test_abastecimento_com_preco_normal_nao_e_anomalo():
    service = AbastecimentoService.__new__(AbastecimentoService)
    service.repository = FakeRepository(media=Decimal("5.00"))

    data = AbastecimentoCreate(
        id_posto=1,
        data_hora=datetime.now(timezone.utc),
        tipo_combustivel=TipoCombustivel.GASOLINA,
        preco_por_litro=Decimal("6.00"),  # +20%
        volume_abastecido=Decimal("40"),
        cpf_motorista="52998224725",
    )

    abastecimento = await service.create_abastecimento(data)

    assert abastecimento.improper_data is False


@pytest.mark.asyncio
async def test_abastecimento_com_preco_acima_do_limiar_e_anomalo():
    service = AbastecimentoService.__new__(AbastecimentoService)
    service.repository = FakeRepository(media=Decimal("5.00"))

    data = AbastecimentoCreate(
        id_posto=1,
        data_hora=datetime.now(timezone.utc),
        tipo_combustivel=TipoCombustivel.GASOLINA,
        preco_por_litro=Decimal("6.50"),  # +30%
        volume_abastecido=Decimal("40"),
        cpf_motorista="52998224725",
    )

    abastecimento = await service.create_abastecimento(data)

    assert abastecimento.improper_data is True
