# 🚀 API de Abastecimentos - Data Lake de Transportes

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **API Gateway** para centralização de dados de abastecimento da frota nacional. Desenvolvida como parte do desafio técnico para vaga de Backend Developer na V-Lab.

---

## 📋 Sobre o Projeto

Este projeto implementa uma API REST robusta para gerenciamento de dados de abastecimento, com foco em:

- **Ingestão de dados** de postos de gasolina e sistemas embarcados
- **Validação rigorosa** com Pydantic (CPF, preços, volumes)
- **Detecção de anomalias** em preços (flag automática para valores 25%+ acima da média)
- **Consultas paginadas** com filtros por tipo de combustível e data
- **Histórico completo** por motorista (CPF)
- **Persistência** em banco relacional (PostgreSQL)
- **Versionamento de schema** com Alembic migrations

---

## 🛠️ Stack Tecnológica

### Core
- **Python 3.11+** - Linguagem principal
- **FastAPI** - Framework web assíncrono de alta performance
- **SQLAlchemy 2.0** - ORM com suporte async
- **PostgreSQL** - Banco de dados relacional
- **Alembic** - Versionamento de schema do banco

### Qualidade & Desenvolvimento
- **Pydantic** - Validação de dados
- **Pytest** - Testes automatizados
- **Ruff/Black** - Linters e formatação de código
- **Docker & Docker Compose** - Containerização e orquestração

### Ferramentas Auxiliares
- **httpx** - Cliente HTTP assíncrono
- **Faker** - Geração de dados de teste
- **python-dotenv** - Gerenciamento de variáveis de ambiente

---

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas com separação clara de responsabilidades:

```
├── app
│   ├── api             # Camada HTTP (routers/endpoints)
│   ├── core            # Regras de negócio (ex: detecção de anomalias)
│   ├── db              # Conexão, sessão e modelos ORM
│   ├── schemas         # Schemas Pydantic (entrada/saída)
│   ├── utils           # Funções utilitárias (ex: validação de CPF)
│   ├── config.py       # Configurações via environment variables
│   └── main.py         # Ponto de entrada da aplicação
│
├── tests               # Testes automatizados (Pytest)
├── scripts             # Scripts auxiliares (ex: carga de dados)
├── docker-compose.yml
├── Dockerfile
└── README.md
```

### Padrões Utilizados
- **Repository Pattern** - Abstração do acesso a dados
- **Service Layer** - Lógica de negócio isolada
- **Dependency Injection** - Injeção de dependências via FastAPI
- **Clean Code** - Funções pequenas, responsabilidade única, nomes descritivos

---

## 🚀 Quick Start

### Pré-requisitos
- **Docker** e **Docker Compose** instalados
- **Git** para clonar o repositório

### 1. Clone o repositório
```bash
git clone https://github.com/TomasNsantos/Technical-Assessment---Backend-Python.git
cd Technical-Assessment---Backend-Python
```

### 2. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

Exemplo de `.env`:
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/abastecimentos
API_VERSION=1.0.0
API_KEY=seu_token_secreto_aqui
```

### 3. Inicie os containers
```bash
docker-compose up -d
```

Isso irá:
- ✅ Criar o banco PostgreSQL
- ✅ Executar as migrations do Alembic automaticamente
- ✅ Iniciar a API na porta 8000
- ✅ Executar o script de carga de dados (opcional)

### 4. Acesse a aplicação

- **API**: http://localhost:8000
- **Documentação interativa (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📡 Endpoints da API

### Health Check
```http
GET /health
```
Retorna status da aplicação e conectividade com banco de dados.

**Resposta:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-01-22T19:30:00+00:00",
  "services": {
    "database": "healthy"
  }
}
```

---

### Criar Abastecimento
```http
POST /api/v1/abastecimentos
Content-Type: application/json
X-API-Key: seu_token_secreto_aqui
```

**Body:**
```json
{
  "id_posto": 123,
  "data_hora": "2025-01-22T14:30:00",
  "tipo_combustivel": "GASOLINA",
  "preco_por_litro": 5.499,
  "volume_abastecido": 45.347,
  "cpf_motorista": "12345678909"
}
```

**Validações automáticas:**
- ✅ CPF válido (algoritmo oficial)
- ✅ Preço > 0
- ✅ Volume > 0
- ✅ Data no formato ISO 8601
- ✅ Tipo de combustível válido (GASOLINA, ETANOL, DIESEL)
- ✅ **Flag de anomalia**: Se preço > 25% da média histórica, marca `improper_data = true`

**Resposta (201 Created):**
```json
{
  "id": 1,
  "id_posto": 123,
  "data_hora": "2025-01-22T14:30:00",
  "tipo_combustivel": "GASOLINA",
  "preco_por_litro": 5.499,
  "volume_abastecido": 45.347,
  "cpf_motorista": "12345678909",
  "improper_data": false,
  "created_at": "2025-01-22T19:30:00+00:00"
}
```

---

### Listar Abastecimentos (Paginado)
```http
GET /api/v1/abastecimentos?page=1&size=10&tipo_combustivel=GASOLINA
```

**Query Parameters:**
- `page` (int, default=1) - Página atual
- `size` (int, default=10) - Itens por página
- `tipo_combustivel` (string, opcional) - Filtrar por tipo (GASOLINA, ETANOL, DIESEL)

**Resposta:**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 10,
  "pages": 10
}
```

---

### Histórico do Motorista
```http
GET /api/v1/motoristas/{cpf}/historico
```

**Exemplo:**
```http
GET /api/v1/motoristas/12345678909/historico
```

**Resposta:**
```json
{
  "cpf_motorista": "12345678909",
  "total_abastecimentos": 15,
  "abastecimentos": [...]
}
```

---

## 🧪 Testes

### Executar testes unitários
```bash
docker-compose exec api pytest
```

### Com cobertura
```bash
docker-compose exec api pytest --cov=app --cov-report=html
```

### Testes específicos
```bash
# Testar validação de CPF
docker-compose exec api pytest tests/test_validators.py

# Testar endpoints
docker-compose exec api pytest tests/test_routers.py
```

---

## 📊 Script de Carga (Stress Test)

O projeto inclui um script para simular carga na API:

```bash
# Via Docker Compose (automático)
docker-compose up load_data

# Manualmente
docker-compose exec api python scripts/load_data.py
```

**Configuração via variáveis de ambiente:**
```env
API_URL=http://api:8000
TOTAL_REQUESTS=100
BATCH_SIZE=10
```

**Funcionalidades:**
- ✅ Gera CPFs válidos automaticamente
- ✅ Cria dados aleatórios mas realistas
- ✅ 15% dos registros têm preços anômalos (para testar flag)
- ✅ Processa requisições em lotes assíncronos
- ✅ Aguarda API ficar disponível (retry automático)
- ✅ Relatório final com métricas de performance

---

## 🗄️ Migrations (Alembic)

### Criar nova migration
```bash
docker-compose exec api alembic revision --autogenerate -m "Descrição da mudança"
```

### Aplicar migrations
```bash
docker-compose exec api alembic upgrade head
```

### Reverter migration
```bash
docker-compose exec api alembic downgrade -1
```

### Ver histórico
```bash
docker-compose exec api alembic history
```

---

## 🔧 Desenvolvimento Local

### Sem Docker

1. **Criar ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

3. **Configurar banco de dados:**
```bash
# Certifique-se de ter PostgreSQL rodando
export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/dbname"
```

4. **Executar migrations:**
```bash
alembic upgrade head
```

5. **Iniciar servidor:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📝 Qualidade de Código

### Formatação automática
```bash
# Black
docker-compose exec api black app/

# Ruff (linting)
docker-compose exec api ruff check app/
```

### Type checking
```bash
docker-compose exec api mypy app/
```

---

## 🐳 Docker

### Estrutura dos containers

```yaml
services:
  db:          # PostgreSQL 16
  api:         # FastAPI application
  load_data:   # Script de carga (opcional)
```

### Comandos úteis

```bash
# Ver logs
docker-compose logs -f api

# Acessar shell do container
docker-compose exec api bash

# Rebuild dos containers
docker-compose up -d --build

# Parar tudo
docker-compose down

# Limpar volumes (⚠️ apaga dados)
docker-compose down -v
```

---

## 📚 Estrutura de Dados

### Tabela: `abastecimentos`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | Integer | ID único (PK, auto-increment) |
| `id_posto` | Integer | Identificador do posto |
| `data_hora` | DateTime(TZ) | Data/hora do abastecimento (ISO 8601) |
| `tipo_combustivel` | Enum | GASOLINA, ETANOL ou DIESEL |
| `preco_por_litro` | Numeric(10,3) | Preço por litro (3 casas decimais) |
| `volume_abastecido` | Numeric(10,3) | Volume em litros |
| `cpf_motorista` | String(11) | CPF do motorista (apenas dígitos) |
| `improper_data` | Boolean | Flag de anomalia (preço 25%+ acima da média) |
| `created_at` | DateTime(TZ) | Timestamp de criação (UTC) |

### Índices
- `id` (PRIMARY KEY)
- `cpf_motorista` (INDEX) - para consultas de histórico

---

## 🎯 Decisões Técnicas

### Por que assíncrono?
- ✅ FastAPI + SQLAlchemy async = máxima performance
- ✅ Suporta alta concorrência sem bloqueio
- ✅ Ideal para I/O bound operations (banco de dados)

### Por que Numeric ao invés de Float?
- ✅ Evita erros de arredondamento em valores monetários
- ✅ Precisão decimal exata (crucial para preços)

### Por que Repository Pattern?
- ✅ Separação de responsabilidades
- ✅ Facilita testes (pode mockar repositories)
- ✅ Lógica de negócio desacoplada do ORM

### Por que Type Hints em tudo?
- ✅ Requisito explícito do desafio
- ✅ Melhora autocomplete e detecção de erros
- ✅ Documentação implícita do código

---

## 🤝 Contribuindo

Embora este seja um projeto de avaliação técnica, sugestões são bem-vindas:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---
