"""Linha de comandos do projeto Morabeza.

Uso: python -m morabeza.cli --ilha Sal
"""

import argparse
import logging
import sys

from morabeza.apoio import faturacao_por_ilha, ler_vendas
from morabeza.config import carregar_config

logger = logging.getLogger(__name__)


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resumo de vendas da Morabeza."
    )

    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Caminho do ficheiro de configuração.",
    )

    parser.add_argument(
        "--ilha",
        help="Ilha para consultar a faturação.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    args = criar_parser().parse_args(argv)

    config = carregar_config(args.config)
    caminho = config["ficheiro_vendas"]
    moeda = config["moeda"]

    vendas = ler_vendas(caminho)

    logger.info("Li %d vendas de %s", len(vendas), caminho)

    totais = faturacao_por_ilha(vendas)

    if args.ilha is not None:
        if args.ilha not in totais:
            logger.error("Ilha desconhecida: %s", args.ilha)
            return 1

        valor = totais[args.ilha]
        print(f"Faturação em {args.ilha}: {valor:.0f} {moeda}")
    else:
        valor = sum(totais.values())
        print(f"Faturação total: {valor:.0f} {moeda}")

    return 0


if __name__ == "__main__":
    sys.exit(main())