# TODO API

Uma API REST para gerenciamento de lista de tarefas (TODO list) desenvolvida com FastAPI, SQLAlchemy e PostgreSQL, seguindo os princípios da Clean Architecture.

## 🏗️ Arquitetura

O projeto segue os princípios da Clean Architecture, organizando o código em camadas bem definidas:

### Estrutura do Projeto

```
src/
├── domain/              # Entidades e regras de negócio
│   └── todo.py         # Entidade Todo com lógica de domínio
├── repos/              # Interfaces dos repositórios
│   └── todo_repository_interface.py
├── infra/              # Infraestrutura e implementações
│   └── database/
│       ├── connection.py    # Configuração da base de dados
│       ├── models.py        # Modelos SQLAlchemy
│       └── todo_repository.py # Implementação do repositório
├── app/                # Serviços da aplicação
│   └── todo_service.py # Lógica de aplicação
└── api/                # Interface HTTP
    ├── schemas/        # Schemas Pydantic
    └── routes.py       # Endpoints da API
```

### Princípios Aplicados

- **Separation of Concerns**: Cada camada tem uma responsabilidade específica
- **Dependency Inversion**: Depende de abstrações, não de implementações
- **Single Responsibility**: Cada classe tem uma única responsabilidade
- **Domain-Driven Design**: A lógica de negócio está no domínio

## 🚀 Funcionalidades

- ✅ Criar novos TODOs
- ✅ Listar TODOs com filtros (status, prioridade)
- ✅ Atualizar TODOs existentes
- ✅ Marcar TODOs como completos/em progresso
- ✅ Deletar TODOs
- ✅ Obter estatísticas dos TODOs
- ✅ Paginação de resultados
- ✅ Validação de dados com Pydantic

## 🛠️ Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM assíncrono para Python
- **PostgreSQL**: Base de dados relacional
- **Pydantic**: Validação de dados e serialização
- **Uvicorn**: Servidor ASGI de alta performance
- **Alembic**: Migrações de base de dados
- **Pytest**: Framework de testes

## 📦 Instalação e Configuração

### 1. Clonar o repositório
```bash
git clone <repository-url>
cd base-api
```

### 2. Configurar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar base de dados
```bash
# Iniciar PostgreSQL com Docker
docker-compose up -d

# Copiar arquivo de configuração
cp .env.example .env
```

### 5. Executar migrações (opcional)
```bash
alembic upgrade head
```

### 6. Iniciar o servidor
```bash
python main.py
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

A documentação interativa da API está disponível em:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔗 Endpoints

### TODOs

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/todos` | Criar novo TODO |
| `GET` | `/api/v1/todos` | Listar TODOs |
| `GET` | `/api/v1/todos/{id}` | Obter TODO por ID |
| `PUT` | `/api/v1/todos/{id}` | Atualizar TODO |
| `PATCH` | `/api/v1/todos/{id}/status` | Atualizar status |
| `DELETE` | `/api/v1/todos/{id}` | Deletar TODO |
| `GET` | `/api/v1/todos/stats` | Estatísticas |

### Exemplos de Uso

#### Criar TODO
```bash
curl -X POST "http://localhost:8000/api/v1/todos" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Estudar FastAPI",
       "description": "Aprender sobre Clean Architecture",
       "priority": "high"
     }'
```

#### Listar TODOs com filtros
```bash
curl "http://localhost:8000/api/v1/todos?status=pending&priority=high&limit=10"
```

#### Atualizar status
```bash
curl -X PATCH "http://localhost:8000/api/v1/todos/{id}/status" \
     -H "Content-Type: application/json" \
     -d '{"status": "completed"}'
```

## 🧪 Testes

### Executar todos os testes
```bash
pytest
```

### Executar testes com cobertura
```bash
pytest --cov=src tests/
```

### Executar testes específicos
```bash
pytest tests/unit/test_todo_domain.py
```

## 🗄️ Schema da Base de Dados

```sql
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status todo_status NOT NULL DEFAULT 'pending',
    priority todo_priority NOT NULL DEFAULT 'medium',
    due_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Enums

- **todo_status**: `pending`, `in_progress`, `completed`
- **todo_priority**: `low`, `medium`, `high`

## 🐳 Docker

### Executar com Docker Compose
```bash
# Iniciar apenas PostgreSQL
docker-compose up -d postgres

# Ou executar toda a aplicação (se configurado)
docker-compose up -d
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/mydatabase
APP_NAME=TODO API
APP_VERSION=1.0.0
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

Para dúvidas ou sugestões, entre em contato através do GitHub Issues.