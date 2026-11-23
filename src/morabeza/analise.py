"""Laboratório 4 (Sessão 7): painel de vendas da Morabeza com pandas e NumPy.

Trabalha com as tabelas completas de 2024 e 2025: vendas, clientes e produtos.
"""
from pathlib import Path

import numpy as np
import pandas as pd


 # já feito: assim podes escrever pasta / "vendas.csv"
    # TODO 1: lê os três ficheiros com pd.read_csv(pasta / "nome.csv").
    #         Nas vendas usa parse_dates=["data"]; nos clientes, parse_dates=["data_registo"].
    #         Devolve (vendas, clientes, produtos), por esta ordem.
def carregar(pasta: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Lê as tabelas de vendas, clientes e produtos."""
    pasta = Path(pasta)

    vendas = pd.read_csv(pasta / "vendas.csv", parse_dates=["data"])
    clientes = pd.read_csv(pasta / "clientes.csv", parse_dates=["data_registo"])
    produtos = pd.read_csv(pasta / "produtos.csv")

    return vendas, clientes, produtos


  # TODO 2: junta às vendas as colunas cliente_id, tipo e ilha dos clientes (merge on="cliente_id")
    #         e as colunas produto_id, nome e categoria dos produtos (merge on="produto_id").
    # TODO 3: cria a coluna total = quantidade * preco_unitario (numa linha, sem ciclos).
def juntar(
    vendas: pd.DataFrame,
    clientes: pd.DataFrame,
    produtos: pd.DataFrame,
) -> pd.DataFrame:
    """Acrescenta os dados do cliente, do produto e o total de cada venda."""
    df = vendas.merge(
        clientes[["cliente_id", "tipo", "ilha"]],
        on="cliente_id",
        how="left",
    )
    df = df.merge(
        produtos[["produto_id", "nome", "categoria"]],
        on="produto_id",
        how="left",
    )
    df["total"] = df["quantidade"] * df["preco_unitario"]

    return df


def faturacao_mensal_por_ilha(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula a faturação por mês e por ilha."""
    dados = df.assign(mes=df["data"].dt.strftime("%Y-%m"))

    return dados.pivot_table(
        index="mes",
        columns="ilha",
        values="total",
        aggfunc="sum",
        fill_value=0,
    )


    # TODO 5: groupby("nome")["total"].sum(), ordena do maior para o menor e fica com os n primeiros.
def top_produtos(df: pd.DataFrame, n: int = 5) -> pd.Series:
    """Devolve os n produtos com maior faturação."""
    faturacao = df.groupby("nome")["total"].sum()

    return faturacao.sort_values(ascending=False).head(n)


    # TODO 6: soma o total por tipo, divide pela soma de tudo, multiplica por 100 e arredonda (round(1)).
def quota_por_tipo(df: pd.DataFrame) -> pd.Series:
    """Calcula a percentagem da faturação por tipo de cliente."""
    t = df.groupby("tipo")["total"].sum()
    faturacao_total = df["total"].sum()
    return (t / faturacao_total * 100).round(1)


    df = df.copy()
    # TODO 7: df["total_com_desconto"] = np.where(condição, valor_se_verdade, valor_se_falso)
    #         Condição: quantidade >= 20. Com desconto: total * 0.95. Sem desconto: total.
def aplicar_desconto(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica 5% de desconto às vendas com pelo menos 20 unidades."""
    df = df.copy()
    df["total_com_desconto"] = np.where(
        df["quantidade"] >= 20,
        df["total"] * 0.95,
        df["total"],
    )

    return df


# ---------------------------------------------------------------- Extensão (opcional)

    # EXTENSÃO: astype("category") nas colunas de texto que se repetem (ilha, tipo, categoria,
    #           nome, produto_id) e pd.to_numeric(..., downcast="integer") em quantidade e preco_unitario.
def otimizar_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """Converte colunas de texto repetitivo em category e reduz os inteiros."""
    """Reduz a memória usada pelas colunas indicadas."""
    df = df.copy()
    categorias = ["ilha", "tipo", "categoria", "nome", "produto_id"]

    df[categorias] = df[categorias].astype("category")
    df["quantidade"] = pd.to_numeric(df["quantidade"], downcast="integer")
    df["preco_unitario"] = pd.to_numeric(
        df["preco_unitario"], downcast="integer"
    )

    return df


   
    # EXTENSÃO: tabela.reset_index().melt(id_vars="mes", var_name="ilha", value_name="total")
def formato_longo(tabela: pd.DataFrame) -> pd.DataFrame:
    """Passa a tabela mensal (uma coluna por ilha) para formato longo: mes, ilha, total."""
    """Devolve uma linha por combinação de mês e ilha."""
    return tabela.reset_index().melt(
        id_vars="mes",
        var_name="ilha",
        value_name="total",
    )
