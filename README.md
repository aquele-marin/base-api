# TODO API

Uma API REST para gerenciamento de lista de tarefas (TODO list) desenvolvida com FastAPI, SQLAlchemy e PostgreSQL, seguindo os princípios da Clean Architecture para repertório.

## 🏗️ Arquitetura

O projeto segue os princípios da Clean Architecture, organizando o código em camadas bem definidas:

### Estrutura do Projeto

```
src/
├── domain/              # Entidades e estruturas de dados
├── repos/              # Repositórios para controle das entidades
├── infra/              # Infraestrutura e implementações
├── app/                # Services da aplicação
└── api/                # Interface HTTP e Schemas
```

### Princípios Aplicados

- **Separation of Concerns**: Cada camada tem uma responsabilidade específica
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
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Executar projeto e dependências
```bash
# Iniciar docker com toda a aplicação
docker-compose up
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

## 🧪 Testes

### Executar todos os testes
```bash
pytest -xvv --disable-warnings
```

## 🐳 Docker

### Executar com Docker Compose
```bash
docker-compose up
```

## 🔧 Configuração

#### Python

- Version 3.12.11

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.