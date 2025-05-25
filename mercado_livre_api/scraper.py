import httpx

async def buscar_produto_ml(termo:str):
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={termo}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
    
    produtos = []
    for item in data.get("results", []):
        produtos.append({
            "nome":item["title"],
            "preco":item["price"],
            "categoria": item.get("category_id", "Desconhecida"),
            "link":item["permalink"]
        })
    return produtos
