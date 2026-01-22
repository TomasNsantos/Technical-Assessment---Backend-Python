from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field, field_validator

from app.models.abastecimento import TipoCombustivel
from app.utils.validators import is_valid_cpf


class AbastecimentoCreate(BaseModel):
    """Schema para criação de abastecimento."""
    
    id_posto: int = Field(..., gt=0, description="ID do posto de abastecimento")
    data_hora: datetime = Field(..., description="Data e hora do abastecimento (ISO 8601)")
    tipo_combustivel: TipoCombustivel = Field(..., description="Tipo de combustível")
    preco_por_litro: Decimal = Field(..., gt=0, decimal_places=3, description="Preço por litro")
    volume_abastecido: Decimal = Field(..., gt=0, decimal_places=3, description="Volume em litros")
    cpf_motorista: str = Field(..., min_length=11, max_length=14, description="CPF do motorista")

    @field_validator("cpf_motorista")
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        """Valida CPF do motorista."""
        if not is_valid_cpf(v):
            raise ValueError("CPF inválido")
        # Retorna apenas dígitos (normaliza)
        return "".join(filter(str.isdigit, v))


class AbastecimentoResponse(BaseModel):
    """Schema para resposta de abastecimento."""
    
    id: int
    id_posto: int
    data_hora: datetime
    tipo_combustivel: TipoCombustivel
    preco_por_litro: Decimal
    volume_abastecido: Decimal
    cpf_motorista: str
    improper_data: bool
    created_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True


class HistoricoResponse(BaseModel):
    """Schema para histórico de abastecimentos do motorista."""
    
    cpf_motorista: str
    total_abastecimentos: int
    abastecimentos: List[AbastecimentoResponse]


class AbastecimentoPagination(BaseModel):
    """Schema para resposta paginada de abastecimentos."""
    
    items: List[AbastecimentoResponse]
    total: int
    page: int
    size: int
    pages: int