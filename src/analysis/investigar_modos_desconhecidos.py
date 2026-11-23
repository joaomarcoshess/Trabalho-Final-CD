from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "processed"

maps = pd.read_csv(DATA_DIR / "maps.csv")
gamemodes = pd.read_csv(DATA_DIR / "gamemodes.csv")

# IDs encontrados nos mapas que não existem em gamemodes
ids_validos = set(gamemodes["id"].dropna().astype(int))
ids_mapas = set(maps["gameMode.id"].dropna().astype(int))

ids_desconhecidos = sorted(ids_mapas - ids_validos)

print("\n========== MODOS DESCONHECIDOS ==========")

for modo_id in ids_desconhecidos:

    registros = maps[
        maps["gameMode.id"] == modo_id
    ]

    print(f"\nID: {modo_id}")
    print("Quantidade de registros:", len(registros))

    print(
        registros[
            ["name", "gameMode.id", "gameMode.name", "disabled"]
        ].to_string(index=False)
    )


# Investigar Upside Showdown
print("\n========== UPSIDE SHOWDOWN ==========")

upside = maps[
    maps["gameMode.name"] == "Upside Showdown"
]

print(upside.to_string(index=False))


# Investigar mapas com o mesmo nome em diferentes modos
print("\n========== MAPAS EM DIFERENTES MODOS ==========")

relacoes = (
    maps.groupby("name")
    .agg(
        quantidade_modos=("gameMode.id", "nunique"),
        modos=("gameMode.name", lambda x: ", ".join(
            sorted(set(x.dropna().astype(str)))
        ))
    )
)

multiplos_modos = relacoes[
    relacoes["quantidade_modos"] > 1
].sort_values("quantidade_modos", ascending=False)

print(multiplos_modos.head(20).to_string())
