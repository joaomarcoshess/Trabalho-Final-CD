from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "processed"

arquivos = ["brawlers", "maps", "gamemodes"]

for nome in arquivos:
    print(f"\n{'=' * 50}")
    print(f"DATASET: {nome.upper()}")
    print("=" * 50)

    df = pd.read_csv(DATA_DIR / f"{nome}.csv")

    print("\nDimensões:", df.shape)

    print("\nColunas:")
    print(df.columns.tolist())

    print("\nPrimeiros registros:")
    print(df.head(3).to_string())

    print("\nTipos de dados:")
    print(df.dtypes)