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

def barras_svg(titulo, dados, cor):
    largura, altura, margem = 560, 330, 55
    maximo = max(dados.values())
    espacamento = (largura - 2 * margem) / len(dados)
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" height="{altura}">', '<rect width="100%" height="100%" fill="#F7FAFC"/>', f'<text x="{largura/2}" y="30" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold" fill="#16324F">{titulo}</text>']
    for i, (rotulo, valor) in enumerate(dados.items()):
        h = valor / maximo * 210
        x = margem + i * espacamento + 12
        y = 270 - h
        partes += [f'<rect x="{x}" y="{y}" width="{espacamento-24}" height="{h}" rx="4" fill="{cor}"/>', f'<text x="{x+(espacamento-24)/2}" y="{y-8}" text-anchor="middle" font-family="Arial" font-size="11">R$ {valor:,.0f}</text>', f'<text x="{x+(espacamento-24)/2}" y="292" text-anchor="middle" font-family="Arial" font-size="10">{rotulo}</text>']
    partes.append('</svg>')
    return ''.join(partes)

(BASE / "dashboard_vendas.svg").write_text(barras_svg("Receita por região", dict(zip(por_regiao["regiao"], por_regiao["receita"])), "#2878B5"), encoding="utf-8")
