# Análise da Popularidade e do Desempenho dos Brawlers em Partidas Casuais de Brawl Stars

## 1. Sobre o projeto

Este trabalho realiza uma análise exploratória de dados sobre a popularidade e o desempenho dos Brawlers em partidas casuais de *Brawl Stars*. O estudo investiga como as métricas de Win Rate, Pick Rate e Use Rate se relacionam, como variam entre modos de jogo e como se comportam ao longo do período analisado.

O período contempla os meses de novembro de 2025 a novembro de 2026. A base comparável utilizada nas análises principais reúne:

- **97 Brawlers** presentes em todos os meses;
- **11 modos de jogo** presentes em todos os meses;
- **13 meses** de observações;
- **13.871 registros**, cada um correspondente a uma combinação de Brawler, modo e mês de referência.

Os registros são dados agregados disponibilizados pelas fontes, e não partidas individuais.

## 2. Fontes de dados

- **[Brawl Time Ninja](https://brawltime.ninja/pt/dashboard):** fonte das métricas mensais de Win Rate, Pick Rate e Use Rate, exportadas em arquivos CSV.
- **[BrawlAPI](https://brawlapi.com/):** fonte de metadados complementares dos Brawlers, modos de jogo e mapas, obtidos em formato JSON. Esses dados foram utilizados principalmente para enriquecer a base com identificadores e classificações, como classe e raridade.

As métricas foram integradas aos metadados por meio dos nomes dos Brawlers, após a padronização dos campos correspondentes.

## 3. Estrutura do repositório

```text
TrabalhoFinalCD/
├── data/
│   ├── raw/
│   │   ├── monthly/       # Exportações mensais em CSV
│   │   └── brawlapi/       # Respostas originais da BrawlAPI em JSON
│   ├── processed/          # Bases consolidadas e metadados tratados
│   └── audit/              # Auditorias da presença de Brawlers e modos
├── notebooks/              # Notebooks de exploração e análise
├── src/
│   ├── extraction/          # Rotinas de coleta da BrawlAPI
│   ├── preprocessing/       # Preparação dos metadados
│   └── analysis/            # Scripts de análise e investigação
├── results/
│   ├── figures/             # Gráficos gerados
│   └── tables/              # Tabelas e relatórios gerados
├── requirements-etapa1.txt
└── README.md
```

## 4. Preparação do ambiente

Requisitos:

- Python 3.10 ou superior;
- pip.

Recomenda-se criar um ambiente virtual antes de instalar as bibliotecas.

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-etapa1.txt
```

### Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-etapa1.txt
```

O arquivo `requirements-etapa1.txt` lista as dependências utilizadas pelas rotinas de análise revisadas. Para executar também a rotina de coleta da BrawlAPI, instale `requests`:

```bash
pip install requests
```

Para abrir e executar os notebooks, instale também Jupyter:

```bash
pip install jupyter
```

## 5. Como executar as análises

Execute os comandos a partir da pasta raiz do repositório (`TrabalhoFinalCD/`). A base processada principal já está incluída em `data/processed/`.

### Etapa 1 — Revisão e análise principal

```bash
python src/analysis/revisao_etapa1.py
```

O script realiza verificações de integridade da base, calcula estatísticas mensais e correlações, compara a Win Rate entre março e abril de 2026 e gera tabelas e figuras em `results/tables/` e `results/figures/`.

### Etapa 2 — Análises complementares

```bash
python src/analysis/etapa2_analises_complementares.py
```

O script gera análises complementares, incluindo:

- amplitude da Win Rate média de cada Brawler entre os modos;
- variação individual de Pick Rate, Use Rate e Win Rate entre o primeiro e o último mês;
- distribuição da Win Rate média por classe;
- gráficos e tabelas correspondentes.

Os arquivos gerados são salvos em `results/figures/` e `results/tables/`.

## 6. Coleta e preparação dos metadados da BrawlAPI

Os arquivos JSON originais utilizados no projeto estão armazenados em `data/raw/brawlapi/`. Caso deseje executar novamente a coleta, utilize:

```bash
python src/extraction/coletar_brawlapi.py
```

A rotina consulta os endpoints de Brawlers, mapas e modos de jogo da BrawlAPI, salva as respostas JSON em `data/raw/brawlapi/` e exporta tabelas CSV para `data/processed/`.

Em seguida, para preparar os metadados:

```bash
python src/preprocessing/preparar_brawlapi.py
```

Esse script organiza os identificadores, gera arquivos tratados em `data/processed/brawlapi/` e produz um relatório de relacionamentos entre mapas e modos de jogo.

**Observação:** a coleta consulta a API no momento da execução. Portanto, os resultados podem diferir dos arquivos históricos incluídos no repositório, caso a API tenha sido atualizada.

## 7. Abordagem analítica

O trabalho utiliza análise exploratória e estatística descritiva. Foram examinadas as métricas de Win Rate, Pick Rate e Use Rate por Brawler, modo de jogo e mês de referência. Também foram realizadas comparações entre classes e raridades, além de análises de correlação de Pearson e Spearman.

Não foram aplicados modelos de Machine Learning na versão final do estudo. A abordagem foi delimitada à análise descritiva e exploratória, de acordo com a estrutura e o nível de agregação dos dados disponíveis.

As atualizações de conteúdo e balanceamento de *Brawl Stars*, incluindo a introdução dos Buffies e ajustes posteriores, são consideradas contexto para a interpretação temporal dos resultados. A análise observacional não permite atribuir mudanças nas métricas exclusivamente a uma atualização específica.

## 8. Limitações

- Os dados são agregados por Brawler, modo e mês de referência; não representam partidas individuais.
- Os arquivos não fornecem contagem de partidas por registro. Por isso, as médias utilizadas são aritméticas simples, sem ponderação pelo volume de partidas.
- O mês de referência do arquivo não necessariamente identifica o período exato em que cada partida ocorreu.
- A base principal não contém a dimensão de mapa.
- A integração de metadados depende da correspondência dos nomes entre as fontes; registros sem correspondência podem ficar sem classificação complementar.
- Correlação indica associação entre variáveis e não demonstra causalidade.

## 9. Resultados e reprodutibilidade

As tabelas, relatórios e visualizações gerados pelos scripts podem ser encontrados em `results/`. As bases brutas, os dados processados e os arquivos de auditoria também estão incluídos no repositório para permitir a inspeção das etapas de preparação.

Para reproduzir as análises principais, mantenha a estrutura de diretórios apresentada neste README e execute os scripts a partir da raiz do projeto, após instalar as dependências.

## 10. Autor

**João Marcos Silva Hess**  
Engenharia de Computação — CEFET-MG, Campus Divinópolis.

---

Projeto acadêmico desenvolvido para a disciplina de Ciência dos Dados.
