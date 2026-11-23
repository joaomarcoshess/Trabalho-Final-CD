
import json
from pathlib import Path

import pandas as pd
import requests


# Caminho principal do projeto
ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "raw" / "brawlapi"
PROCESSED_DIR = ROOT / "data" / "processed"

BASE_URL = "https://api.brawlapi.com/v1"

FONTES = {
    "brawlers": f"{BASE_URL}/brawlers",
    "maps": f"{BASE_URL}/maps",
    "gamemodes": f"{BASE_URL}/gamemodes"
}


def coletar_dados(nome, url):
    print(f"\nColetando: {nome}")

    resposta = requests.get(url, timeout=30)
    resposta.raise_for_status()

    dados = resposta.json()

    # Verifica a estrutura da resposta
    if not isinstance(dados, dict) or "list" not in dados:
        raise ValueError(
            f"Formato inesperado na resposta de {nome}"
        )

    registros = dados["list"]

    if not isinstance(registros, list) or not registros:
        raise ValueError(
            f"Nenhum registro encontrado para {nome}"
        )

    # Salva o JSON original
    arquivo_json = RAW_DIR / f"{nome}.json"

    with arquivo_json.open("w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    # Converte para DataFrame
    df = pd.json_normalize(registros)

    # Salva o CSV
    arquivo_csv = PROCESSED_DIR / f"{nome}.csv"

    df.to_csv(
        arquivo_csv,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Registros encontrados: {len(df)}")
    print(f"Colunas: {len(df.columns)}")
    print(f"JSON salvo: {arquivo_json}")
    print(f"CSV salvo: {arquivo_csv}")

    return df


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    resultados = {}

    for nome, url in FONTES.items():
        try:
            resultados[nome] = coletar_dados(nome, url)

        except (requests.RequestException, ValueError) as erro:
            print(f"ERRO ao coletar {nome}: {erro}")

    print("\n========== RESUMO DA COLETA ==========")

    for nome, df in resultados.items():
        print(f"{nome}: {len(df)} registros")

    print("\nColeta finalizada!")


if __name__ == "__main__":
    main()
