import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

# Base para os modelos SQLAlchemy
Base = declarative_base()

# Configuração da base de dados
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://user:password@localhost:5432/mydatabase"
)

# Engine assíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Para debugging - remover em produção
    future=True
)

# Session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db_session():
    """Dependency que retorna uma sessão de base de dados"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Inicializa as tabelas da base de dados"""
    # Import necessário aqui para evitar import circular
    from src.infra.database.models import TodoModel
    
    async with engine.begin() as conn:
        # Criar todas as tabelas
        await conn.run_sync(Base.metadata.create_all)