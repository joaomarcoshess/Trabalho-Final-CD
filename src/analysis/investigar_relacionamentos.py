from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "processed"

brawlers = pd.read_csv(DATA_DIR / "brawlers.csv")
maps = pd.read_csv(DATA_DIR / "maps.csv")
gamemodes = pd.read_csv(DATA_DIR / "gamemodes.csv")


# 1. Investigar nomes repetidos nos mapas

repetidos = (
    maps.groupby("name")
    .agg(
        registros=("id", "count"),
        modos=("gameMode.name", "nunique"),
        ativos=("disabled", lambda x: (~x).sum())
    )
    .query("registros > 1")
    .sort_values("registros", ascending=False)
)

print("Quantidade de nomes repetidos:", len(repetidos))
print("\nMaiores ocorrências:")
print(repetidos.head(15))


# 2. Investigar mapas ativos por modo

mapas_ativos = maps[maps["disabled"] == False]

print("Total de mapas ativos:", len(mapas_ativos))

print("\nMapas ativos por modo:")
print(
    mapas_ativos["gameMode.name"]
    .value_counts()
    .head(20)
)


# 3. Verificar relacionamento entre IDs

ids_modos = set(gamemodes["id"])
ids_modos_mapas = set(maps["gameMode.id"].dropna())

ids_sem_correspondencia = ids_modos_mapas - ids_modos

print("IDs de modos encontrados nos mapas:", len(ids_modos_mapas))
print("IDs sem correspondência:", len(ids_sem_correspondencia))

if ids_sem_correspondencia:
    print("IDs não encontrados:")
    print(sorted(ids_sem_correspondencia))
else:
    print("Todos os IDs dos mapas possuem correspondência!")


# 4. Comparar nomes dos modos

nomes_mapas = set(maps["gameMode.name"].dropna())
nomes_modos = set(gamemodes["name"].dropna())

print("Nomes de modos nos mapas:", len(nomes_mapas))
print("Nomes na tabela gamemodes:", len(nomes_modos))

print("\nNomes presentes nos mapas, mas ausentes em gamemodes:")
print(sorted(nomes_mapas - nomes_modos))


# 5. Verificar colunas completamente vazias

for nome, df in [
    ("Brawlers", brawlers),
    ("Maps", maps),
    ("Gamemodes", gamemodes)
]:
    vazias = df.columns[df.isna().all()].tolist()

    print(f"{nome}: {vazias}")
