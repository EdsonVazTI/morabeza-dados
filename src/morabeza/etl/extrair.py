"""Lab 5 · Extrair de quatro fontes.

As fontes estão em data/fontes_s1_2025/. Testa com:
    pytest tests/test_etl_lab5.py -v
"""

import json
import sqlite3
from contextlib import closing

import pandas as pd



"""Lê o CSV de vendas com TUDO como texto (dtype=str), para não perder
    informação antes de limpar."""
def ler_vendas_csv(caminho):
    return pd.read_csv(caminho, dtype=str)



"""Lê a folha 'produtos' do Excel."""
def ler_produtos_excel(caminho):
    return pd.read_excel(caminho, sheet_name="produtos")


"""SELECT * FROM clientes. Dica: pd.read_sql_query(sql, conn)"""
def ler_clientes_sqlite(caminho):
    with closing(sqlite3.connect(caminho)) as conn:
        return pd.read_sql_query("SELECT * FROM clientes", conn)


"""O ficheiro imita a resposta de uma API: os registos estão em 'dados'.
    Se 'estado' não for 'ok', levanta ValueError."""
def ler_promocoes_json(caminho):
    with open(caminho, encoding="utf-8") as ficheiro:
        resposta = json.load(ficheiro)

    if resposta.get("estado") != "ok":
        raise ValueError("A resposta das promoções tem um estado inválido.")

    return pd.DataFrame(resposta["dados"])