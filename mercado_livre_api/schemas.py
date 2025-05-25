from pydantic import BaseModel

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    categoria: str
    link: str

    class Config:
        orm_mode = True
        