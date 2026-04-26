# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 14:41:11 2026

@author: Cacob
"""
# PASSO 1


import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pingouin as pg
from lets_plot import *


LetsPlot.setup_html(no_js=True)

plt.style.use("https://raw.githubusercontent.com/aeturrell/core_python/main/plot_style.txt")


# PASSO 2 (Setando o python pra funfar com esses dados)


# Código para tornar o diretório da base de dados relativo (Executar em qualquer PC)
diretorio_base = Path(__file__).resolve().parent

# Caminho relativo até a planilha Empresas.xlsx
caminho_empresas = diretorio_base / "dados" / "Empresas.xlsx"

# Importa a planilha
empresas = pd.read_excel(caminho_empresas)
empresas.info()

# Planilha de empresas sem dados faltantes na coluna "talent6"
empresas = empresas.dropna(subset=['talent6'])



# PASSO 3 (Criando as colunas: operations, monitor, people & target. Colunas essas que serão uma média dos critérios semelhantes entre as várias colunas
# o objetivo aqui é filtrar todos os caras que são parecidos, e guardarem em uma unica coluna q é a média geral)


# Mandando o Python fazer uma lista com o nome das colunas da database que estou trabalhando, aqui meio que funciona como uma "seleção" do que quero mexer
# Para depois com os objetos que criei, usar metodos para tirar algumas medidas de estatística descritiva

coluna_operations = ["lean1", "lean2"]

coluna_monitor = ["perf1", "perf2", "perf3", "perf4", "perf5"]

coluna_people = ["talent1", "talent2", "talent3", "talent4", "talent5", "talent6"]

coluna_target = ["perf6", "perf7", "perf8", "perf9", "perf10"]

empresas["operations"] = empresas[coluna_operations].mean(axis=1).round(2) # <-- axis=1 aqui faz com que o python calcule linha por linha, diferente de axis=0, que calcula média da amostra total da coluna
empresas["monitor"] = empresas[coluna_monitor].mean(axis=1).round(2)
empresas["people"] = empresas[coluna_people].mean(axis=1).round(2)
empresas["target"] = empresas[coluna_target].mean(axis=1).round(2)
empresas["management"] = empresas[["operations", "monitor", "people", "target"]].mean(axis=1).round(2)


# PASSO 4 (preparando tabela para rankear os países de acordo com cada critério)


empresas_sem_colunas = empresas[["country", "operations", "monitor", "people", "target", "management" ]]

empresas_agrupado = empresas_sem_colunas.groupby("country").mean(numeric_only=True).round(2)

empresas_agrupado.sort_values(by=["management"], ascending = False)









