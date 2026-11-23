
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "processed"


def carregar(nome):
    return pd.read_csv(DATA_DIR / f"{nome}.csv")


def auditar_brawlers():
    df = carregar("brawlers")

    print("\n========== BRAWLERS ==========")

    print("Total de registros:", len(df))
    print("IDs únicos:", df["id"].nunique())
    print("Nomes únicos:", df["name"].nunique())

    print("\nValores ausentes:")
    print(df.isna().sum().sort_values(ascending=False).head(10))

    print("\nClasses:")
    print(df["class.name"].value_counts(dropna=False))

    print("\nRaridades:")
    print(df["rarity.name"].value_counts(dropna=False))


def auditar_maps():
    df = carregar("maps")

    print("\n========== MAPS ==========")

    print("Total de registros:", len(df))
    print("IDs únicos:", df["id"].nunique())
    print("Nomes únicos:", df["name"].nunique())

    print("\nMapas desativados:")
    print(df["disabled"].value_counts(dropna=False))

    print("\nModos associados aos mapas:")
    print(df["gameMode.name"].value_counts(dropna=False))

    print("\nIDs duplicados:", df["id"].duplicated().sum())


def auditar_gamemodes():
    df = carregar("gamemodes")

    print("\n========== GAMEMODES ==========")

    print("Total de registros:", len(df))
    print("IDs únicos:", df["id"].nunique())

    print("\nModos disponíveis:")
    print(df[["id", "name", "disabled"]].to_string(index=False))

    print("\nValores ausentes:")
    print(df.isna().sum().sort_values(ascending=False).head(10))


def main():
    auditar_brawlers()
    auditar_maps()
    auditar_gamemodes()


if __name__ == "__main__":
    main()
