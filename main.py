from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import todo_router
from src.infra.database.connection import init_db

app = FastAPI(
    title="TODO API",
    description="API de TO-DO list seguindo Clean Architecture",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das rotas
app.include_router(todo_router, prefix="/api/v1", tags=["todos"])

@app.on_event("startup")
async def startup_event():
    """Inicializa a base de dados na inicialização da aplicação"""
    await init_db()

@app.get("/", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "TODO API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )