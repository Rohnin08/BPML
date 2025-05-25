from fastapi import FastAPI
from scraper import buscar_produto_ml
from models import Produto, Base
from database import engine, async_session
from schemas import ProdutoBase
from sqlalchemy.future import select

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def root():
    return {"msg": "API: Comparador de preços do Mercado Livre"}

@app.get("/buscar/{termo}", response_model=list[ProdutoBase])
async def buscar(termo:str):
    produtos = await buscar_produto_ml(termo)
    async with async_session() as session:
        for p in produtos:
            produto = Produto(**p)
            session.add(produto)
        await session.commit()
    return produtos

@app.get("/comparar", response_model=list[ProdutoBase])
async def comparar():
    async with async_session() as session:
        result = await session.execute(select(Produto).order_by(Produto.preco.asc()))
        produtos = result.scalars().all()
        return produtos

