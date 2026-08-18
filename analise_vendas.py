from pathlib import Path

import pandas as pd


BASE = Path(__file__).parent
dados = pd.read_csv(BASE / "vendas_exemplo.csv", parse_dates=["data"])

dados["receita"] = dados["quantidade"] * dados["preco_unitario"]

indicadores = pd.DataFrame(
    {
        "indicador": ["Receita total", "Pedidos", "Ticket médio"],
        "valor": [dados["receita"].sum(), dados["pedido_id"].nunique(), dados.groupby("pedido_id")["receita"].sum().mean()],
    }
)

por_regiao = dados.groupby("regiao", as_index=False)["receita"].sum().sort_values("receita", ascending=False)
por_categoria = dados.groupby("categoria", as_index=False)["receita"].sum().sort_values("receita", ascending=False)
por_produto = dados.groupby("produto", as_index=False)["receita"].sum().sort_values("receita", ascending=False)

saida = BASE / "resultados"
saida.mkdir(exist_ok=True)
indicadores.to_csv(saida / "indicadores.csv", index=False)
por_regiao.to_csv(saida / "receita_por_regiao.csv", index=False)
por_categoria.to_csv(saida / "receita_por_categoria.csv", index=False)
por_produto.to_csv(saida / "receita_por_produto.csv", index=False)

print(indicadores.to_string(index=False))
print("\nReceita por região:\n", por_regiao.to_string(index=False))
