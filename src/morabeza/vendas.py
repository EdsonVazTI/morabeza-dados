"""Vendas da Morabeza em Python idiomático (Sessão 2).

Cada venda passa a ser um objeto Venda (dataclass) em vez de um dicionário.
Linhas com erros levantam VendaInvalida e são postas de parte na leitura.
"""
from __future__ import annotations

import csv
import time
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date

ILHAS_SERVIDAS = {"Santiago", "São Vicente", "Sal", "Boa Vista", "Fogo", "Santo Antão"}


class VendaInvalida(Exception):
    """Uma linha do ficheiro de vendas não pode ser transformada numa Venda."""


@dataclass(frozen=True)
class Venda:
    venda_id: str
    data: date
    cliente_id: str
    ilha: str
    categoria: str
    quantidade: int
    preco_unitario: int

    @property
    def total(self) -> int:
        """Valor da venda em escudos."""
        # TODO 1: devolve a quantidade vezes o preço unitário (usa self.).
        raise NotImplementedError("Venda.total ainda não está feita")


def criar_venda(linha: dict[str, str]) -> Venda:
    """Converte uma linha do CSV numa Venda, ou levanta VendaInvalida."""
    # TODO 2: dentro de um try, converte quantidade e preco_unitario com int()
    #         e a data com date.fromisoformat(). Se der ValueError, levanta
    #         VendaInvalida (raise VendaInvalida("...") from erro).
    # TODO 3: levanta VendaInvalida se a quantidade ou o preço não forem > 0,
    #         ou se linha["ilha"] não estiver em ILHAS_SERVIDAS.
    # TODO 4: devolve Venda(...) com os valores já convertidos.
    raise NotImplementedError("criar_venda ainda não está feita")


def ler_vendas(caminho: str) -> Iterator[Venda]:
    """Gerador: devolve, uma a uma, as vendas válidas do ficheiro. As inválidas são ignoradas."""
    # TODO 5: abre o ficheiro e percorre csv.DictReader. Para cada linha,
    #         tenta yield criar_venda(linha); se der VendaInvalida, continue.
    #         Repara: é um gerador, por isso usa yield e não return.
    raise NotImplementedError("ler_vendas ainda não está feita")


def contar_invalidas(caminho: str) -> int:
    """Número de linhas do ficheiro que não dão uma Venda válida."""
    # TODO 6: igual a ler_vendas, mas em vez de devolver vendas conta quantas
    #         linhas levantam VendaInvalida e devolve esse número.
    raise NotImplementedError("contar_invalidas ainda não está feita")


def vendas_acima(vendas: Iterable[Venda], limite: int) -> list[Venda]:
    """Vendas com total maior do que o limite, numa compreensão de lista."""
    # TODO 7: uma só linha com uma compreensão de lista: [v for v in ... if ...]
    raise NotImplementedError("vendas_acima ainda não está feita")


def total_por(vendas: Iterable[Venda], chave: Callable[[Venda], str]) -> dict[str, int]:
    """Soma dos totais agrupada pela função chave. Ex.: total_por(vendas, lambda v: v.ilha)."""
    # TODO 8: igual a faturacao_por_ilha da Sessão 1, mas a chave do dicionário
    #         é chave(v) em vez de v["ilha"]. Assim a mesma função serve para
    #         agrupar por ilha, por categoria ou por mês.
    raise NotImplementedError("total_por ainda não está feita")


# ---------------------------------------------------------------- Extensão (opcional)

def top_n(totais: dict[str, int], n: int) -> list[tuple[str, int]]:
    """Os n pares (chave, total) com maior total, do maior para o menor."""
    # EXTENSÃO: sorted(totais.items(), key=lambda par: ..., reverse=True) e depois [:n]
    raise NotImplementedError("Extensão por fazer")


@contextmanager
def cronometro(nome: str):
    """Mede o tempo de um bloco. Uso: with cronometro("leitura"): ..."""
    # EXTENSÃO: guarda time.perf_counter() antes do yield e, num finally,
    #           imprime f"{nome}: {segundos:.3f} s".
    raise NotImplementedError("Extensão por fazer")
    yield
