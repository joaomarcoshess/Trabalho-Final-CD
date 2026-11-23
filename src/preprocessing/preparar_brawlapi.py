from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "data" / "processed"
OUTPUT_DIR = ROOT / "data" / "processed" / "brawlapi"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def carregar(nome):
    return pd.read_csv(RAW_DIR / f"{nome}.csv")


def preparar_brawlers():
    df = carregar("brawlers")

    # Remover colunas completamente vazias
    df = df.dropna(axis=1, how="all")

    # Padronizar tipos dos identificadores
    df["id"] = pd.to_numeric(df["id"], errors="raise").astype("int64")

    # Verificar unicidade
    assert df["id"].is_unique

    df.to_csv(
        OUTPUT_DIR / "brawlers_tratados.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("Brawlers preparados:", len(df))


def preparar_maps():
    df = carregar("maps")

    df["id"] = pd.to_numeric(df["id"], errors="raise").astype("int64")
    df["gameMode.id"] = pd.to_numeric(
        df["gameMode.id"], errors="coerce"
    )

    assert df["id"].is_unique

    df.to_csv(
        OUTPUT_DIR / "maps_tratados.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("Maps preparados:", len(df))


def preparar_gamemodes():
    df = carregar("gamemodes")

    # Remover colunas completamente vazias
    df = df.dropna(axis=1, how="all")

    df["id"] = pd.to_numeric(df["id"], errors="raise").astype("int64")
    df["scId"] = pd.to_numeric(df["scId"], errors="coerce")

    assert df["id"].is_unique

    df.to_csv(
        OUTPUT_DIR / "gamemodes_tratados.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("Gamemodes preparados:", len(df))


def gerar_relatorio_relacionamentos():
    maps = carregar("maps")
    gamemodes = carregar("gamemodes")

    ids_validos = set(gamemodes["id"])
    ids_mapas = set(maps["gameMode.id"].dropna())

    ids_sem_correspondencia = ids_mapas - ids_validos

    relatorio = (
        maps[maps["gameMode.id"].isin(ids_sem_correspondencia)]
        .copy()
    )

    relatorio.to_csv(
        OUTPUT_DIR / "map_gamemode_unmatched.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(
        "Registros com modo sem correspondência:",
        len(relatorio)
    )


def main():
    print("\n===== PREPARAÇÃO DA BRAWLAPI =====")

    preparar_brawlers()
    preparar_maps()
    preparar_gamemodes()
    gerar_relatorio_relacionamentos()

    print("\nPreparação concluída!")


if __name__ == "__main__":
    main()
