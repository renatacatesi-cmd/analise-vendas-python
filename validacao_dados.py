import pandas as pd


COLUNAS_OBRIGATORIAS = {"data", "produto", "categoria", "regiao", "quantidade", "preco_unitario"}


def validar_vendas(caminho="vendas_exemplo.csv"):
    df = pd.read_csv(caminho)
    faltantes = COLUNAS_OBRIGATORIAS.difference(df.columns)
    erros = []
    if faltantes:
        erros.append(f"Colunas ausentes: {sorted(faltantes)}")
        return erros
    if df[list(COLUNAS_OBRIGATORIAS)].isna().any().any():
        erros.append("Existem valores nulos em campos obrigatórios.")
    if (df["quantidade"] <= 0).any():
        erros.append("Quantidade deve ser maior que zero.")
    if (df["preco_unitario"] <= 0).any():
        erros.append("Preço unitário deve ser maior que zero.")
    if df.duplicated().any():
        erros.append("Existem registros duplicados.")
    return erros


if __name__ == "__main__":
    inconsistencias = validar_vendas()
    print("Dados aprovados." if not inconsistencias else "\n".join(inconsistencias))
