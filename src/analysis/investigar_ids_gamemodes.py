from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "processed"

maps = pd.read_csv(DATA_DIR / "maps.csv")
gamemodes = pd.read_csv(DATA_DIR / "gamemodes.csv")

# Padronização dos identificadores para comparação
for coluna in ["id", "scId"]:
    gamemodes[coluna] = pd.to_numeric(
        gamemodes[coluna], errors="coerce"
    )

for coluna in ["gameMode.id", "gameMode.scId"]:
    maps[coluna] = pd.to_numeric(
        maps[coluna], errors="coerce"
    )


print("\n========== TABELA GAMEMODES ==========")

print(
    gamemodes[["id", "scId", "name", "disabled"]]
    .sort_values("name")
    .to_string(index=False)
)


print("\n========== RELACIONAMENTO POR NOME ==========")

relacoes = (
    maps.groupby("gameMode.name")
    .agg(
        ids_api=("gameMode.id", lambda x:
                 sorted(x.dropna().unique().tolist())),
        ids_sc=("gameMode.scId", lambda x:
                sorted(x.dropna().unique().tolist()))
    )
    .reset_index()
)

print(relacoes.to_string(index=False))


print("\n========== VERIFICAÇÃO POR SCID ==========")

ids_sc_modos = set(gamemodes["scId"].dropna())
ids_sc_mapas = set(maps["gameMode.scId"].dropna())

print("SCIDs nos mapas:", len(ids_sc_mapas))
print("SCIDs nos modos:", len(ids_sc_modos))

print(
    "SCIDs dos mapas sem correspondência:",
    sorted(ids_sc_mapas - ids_sc_modos)
)


print("\n========== NOMES COM MÚLTIPLOS IDS ==========")

multiplos = relacoes[
    relacoes["ids_api"].apply(len) > 1
]

print(multiplos.to_string(index=False))
