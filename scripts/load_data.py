"""Script de carga para API de abastecimentos."""
import asyncio
import os
import random
from datetime import datetime

import httpx
from faker import Faker

# Faker em pt_BR para CPF válido
fake = Faker("pt_BR")

# Configurações via variáveis de ambiente
API_URL = os.getenv("API_URL", "http://localhost:8000")
TOTAL_REQUESTS = int(os.getenv("TOTAL_REQUESTS", "100"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10"))


def gerar_abastecimento() -> dict:
    """Gera dados de abastecimento aleatórios e válidos."""
    tipo = random.choice(["GASOLINA", "ETANOL", "DIESEL"])

    precos_base = {
        "GASOLINA": 5.50,
        "ETANOL": 4.00,
        "DIESEL": 6.20,
    }

    base = precos_base[tipo]

    # 15% de chance de anomalia (25–50% acima da média)
    preco = (
        base * random.uniform(1.25, 1.50)
        if random.random() < 0.15
        else base * random.uniform(0.95, 1.05)
    )

    return {
        "id_posto": random.randint(1, 500),
        "data_hora": fake.date_time_between(
            start_date="-1y", end_date="now"
        ).isoformat(),
        "tipo_combustivel": tipo,
        "preco_por_litro": round(preco, 3),
        "volume_abastecido": round(random.uniform(15.0, 75.0), 3),
        "cpf_motorista": fake.cpf(),  # CPF válido pelo Faker
    }


async def enviar_requisicao(
    client: httpx.AsyncClient, numero: int
) -> dict:
    """Envia requisição para a API."""
    try:
        response = await client.post(
            f"{API_URL}/api/v1/abastecimentos",
            json=gerar_abastecimento(),
            timeout=15.0,
        )

        status = "sucesso" if response.status_code == 201 else "erro"
        print(
            f"{'✓' if status == 'sucesso' else '✗'} "
            f"[{numero:03d}/{TOTAL_REQUESTS:03d}] {status.upper()}"
        )
        return {"status": status, "code": response.status_code}

    except Exception as e:
        print(
            f"✗ [{numero:03d}/{TOTAL_REQUESTS:03d}] "
            f"EXCEÇÃO: {type(e).__name__}"
        )
        return {"status": "excecao", "erro": str(e)}


async def aguardar_api(client: httpx.AsyncClient) -> bool:
    """Aguarda API ficar disponível."""
    print("⏳ Aguardando API...")

    for _ in range(30):
        try:
            response = await client.get(f"{API_URL}/docs", timeout=5.0)
            if response.status_code == 200:
                print("✓ API disponível!\n")
                return True
        except Exception:
            pass

        await asyncio.sleep(2)

    print("✗ API não respondeu")
    return False


async def executar_lote(
    client: httpx.AsyncClient, inicio: int, tamanho: int
) -> list:
    """Executa um lote de requisições em paralelo."""
    tarefas = [
        enviar_requisicao(client, inicio + i + 1)
        for i in range(tamanho)
    ]
    return await asyncio.gather(*tarefas, return_exceptions=True)


async def main():
    """Executa carga de dados."""
    print("=" * 60)
    print("🚀 CARGA DE DADOS - API DE ABASTECIMENTOS")
    print("=" * 60)
    print(f"Target:      {API_URL}")
    print(f"Requisições: {TOTAL_REQUESTS}")
    print(f"Lote:        {BATCH_SIZE}")
    print("=" * 60 + "\n")

    async with httpx.AsyncClient() as client:
        if not await aguardar_api(client):
            return

        inicio_tempo = datetime.now()
        resultados = []

        for i in range(0, TOTAL_REQUESTS, BATCH_SIZE):
            tamanho = min(BATCH_SIZE, TOTAL_REQUESTS - i)
            lote = await executar_lote(client, i, tamanho)

            for r in lote:
                resultados.append(
                    r if not isinstance(r, Exception)
                    else {"status": "excecao"}
                )

            if i + BATCH_SIZE < TOTAL_REQUESTS:
                await asyncio.sleep(2)

        tempo_total = (datetime.now() - inicio_tempo).total_seconds()
        sucessos = sum(
            1 for r in resultados if r.get("status") == "sucesso"
        )

        print("\n" + "=" * 60)
        print("✅ CONCLUÍDO!")
        print("=" * 60)
        print(
            f"Sucessos:    {sucessos}/{TOTAL_REQUESTS} "
            f"({sucessos / TOTAL_REQUESTS * 100:.1f}%)"
        )
        print(f"Erros:       {TOTAL_REQUESTS - sucessos}/{TOTAL_REQUESTS}")
        print(f"Tempo:       {tempo_total:.2f}s")
        print(
            f"Throughput:  {TOTAL_REQUESTS / tempo_total:.2f} req/s"
        )
        print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n  Interrompido pelo usuário")
