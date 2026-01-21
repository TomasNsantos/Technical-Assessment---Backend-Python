from datetime import datetime
from enum import Enum as PyEnum
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Enum, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TipoCombustivel(str, PyEnum):
    GASOLINA = "GASOLINA"
    ETANOL = "ETANOL"
    DIESEL = "DIESEL"


class Abastecimento(Base):
    
    __tablename__ = "abastecimentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_posto: Mapped[int] = mapped_column(Integer, nullable=False)
    data_hora: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False
    )
    tipo_combustivel: Mapped[TipoCombustivel] = mapped_column(
        Enum(TipoCombustivel, name="tipo_combustivel_enum"),
        nullable=False,
    )
    preco_por_litro: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), 
        nullable=False
    )
    volume_abastecido: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), 
        nullable=False
    )
    cpf_motorista: Mapped[str] = mapped_column(
        String(11), 
        nullable=False, 
        index=True
    )
    improper_data: Mapped[bool] = mapped_column(
        Boolean, 
        default=False, 
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )