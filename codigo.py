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
from matplotlib.ticker import PercentFormatter

plt.style.use("ggplot")
plt.rcParams["font.family"] = "monospace"



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


médias_por_critério = empresas[["country", "operations", "monitor", "people", "target", "management" ]]

ranking_países = médias_por_critério.groupby("country").mean(numeric_only=True).round(2)

ranking_ordenado = ranking_países.sort_values(by=["management"], ascending = True)


# PASSO 5 (Plotando os valores dos países em um gráfico de colunas)

plt.figure(figsize=(14, 6))

plt.barh(
    ranking_ordenado.index, # categoria utilizada para a plotagem do gráfico (países)
    ranking_ordenado["management"], # critério utilizado no rankeamento
    color="#688dd4", # cor do gráfico ¯\_(ツ)_/¯
    height=0.6, 
    edgecolor="black"
)

# Ajustando o tamanho dos nomes dos países
plt.tick_params(axis="y", labelsize=9)

# Ajusta os números no eixo x
plt.tick_params(axis="x", labelsize=10)

# Título e rótulo do eixo x
plt.title("Qualidade média da administração por país", fontsize=14, loc = "center")
plt.xlabel("Nota média de administração", fontsize=12)

# Deixa espaço à esquerda para os nomes dos países
plt.subplots_adjust(left=0.35)

# nota de administração das empresas, indo numa escala de 0 a 5
plt.xlim(0, 5)

plt.show()

# Passo 6 Comparando as notas das empresas do Brasil, com a outros países

separações = np.linspace(1, 5, 25) # Definindo que o histograma vai de 1 a 5 dividido em 25 pedaçinhos ( intervalos de 0.2 em 0.2)


# Pegando a média das empresas de cada país, e transformando num vetor
brasil_empresas = médias_por_critério[médias_por_critério["country"] == "Brazil"]["management"].dropna() # Vendo a distribuição de management quando country == Brazil
india_empresas = médias_por_critério[médias_por_critério["country"] == "India"]["management"].dropna() # Vendo a distribuição de management quando country == India
Mexico_empresas = médias_por_critério[médias_por_critério["country"] == "Mexico"]["management"].dropna() # Vendo a distribuição de management quando country == Mexico
Reino_Unido_empresas = médias_por_critério[médias_por_critério["country"] == "Great Britain"]["management"].dropna()
Estados_Unidos_empresas = médias_por_critério[médias_por_critério['country'] == 'United States']['management'].dropna()

# Transformando o número de empresas vistas em frequencia relativa, mas por que disso?
# Bom, não faria sentido eu dizer que o Brasil é melhor que a Índia em um cenário em que o 
# Brasil tenha 100 empresas, e a Índia só 50, supondo hipotéticamente que ambos os países possuem
# Empresas com notas identicas, então por frequencia, fica mais claro ver no gráfico que ambos seriam equivalentes

pesos_brasil = np.ones(len(brasil_empresas)) / len(brasil_empresas) # fração 1/n empresas <- peso para cada empresa no gráfico
pesos_india = np.ones(len(india_empresas)) / len(india_empresas) 
pesos_Mexico = np.ones(len(Mexico_empresas))/ len(Mexico_empresas) 
pesos_Reino_Unido = np.ones(len(Reino_Unido_empresas))/ len(Reino_Unido_empresas)
pesos_Estados_Unidos = np.ones(len(Estados_Unidos_empresas))/ len(Estados_Unidos_empresas)


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2) # Quebrando o plot em 4 pedaços para 4 gráficos diferentes 


#comparação das empresas Brasil X India em um histograma
plt.subplots_adjust(hspace=0.50, wspace=0.25)

ax1.hist(brasil_empresas, bins=separações, weights=pesos_brasil,
         alpha=0.8,label="Brazil",color="#6cc47c",edgecolor="black")

ax1.hist(india_empresas,bins=separações,weights=pesos_india, alpha=0.6, 
         label="India",color="#d65a31",edgecolor="black")

ax1.legend(loc="upper right", fontsize="small")
ax1.set_title("Distribuição proporcional das empresas\npor nota Brasil x Índia", fontsize=7.5)
ax1.tick_params(axis="y", labelsize=8)
ax1.tick_params(axis="x", labelsize=8)
ax1.set_xlim(1, 5)
ax1.yaxis.set_major_formatter(PercentFormatter(1.0)) # <- usando pacote que importei para formar em %

#
#
#

#comparação das empresas Brasil X Mexico em um histograma
ax2.hist(brasil_empresas, bins=separações, weights=pesos_brasil,
         alpha=0.7,label="Brazil",color="#6cc47c",edgecolor="black")

ax2.hist(Mexico_empresas,bins=separações,weights=pesos_Mexico, alpha=0.5, 
         label="Mexico",color="#265425",edgecolor="black")

ax2.legend(loc="upper right", fontsize="small")
ax2.set_title("Distribuição proporcional das empresas\npor nota Brasil x Mexico", fontsize=7.5)
ax2.tick_params(axis="y", labelsize=8)
ax2.tick_params(axis="x", labelsize=8)
ax2.set_xlim(1, 5)
ax2.yaxis.set_major_formatter(PercentFormatter(1.0)) 

#
#
#

#comparação das empresas Brasil X Reino Unido em um histograma
ax3.hist(brasil_empresas, bins=separações, weights=pesos_brasil,
         alpha=0.7,label="Brazil",color="#6cc47c",edgecolor="black")

ax3.hist(Reino_Unido_empresas,bins=separações,weights=pesos_Reino_Unido, alpha=0.5, 
         label="Reino Unido",color="#11149e",edgecolor="black")

ax3.legend( fontsize= 'small', bbox_to_anchor=(0.5, -0.3, 0.1, 0.1) )
ax3.set_title("Distribuição proporcional das empresas\npor nota Brasil x Reino Unido", fontsize=7.5)
ax3.tick_params(axis="y", labelsize=8)
ax3.tick_params(axis="x", labelsize=8)
ax3.set_xlim(1, 5)
ax3.yaxis.set_major_formatter(PercentFormatter(1.0)) 

#
#
#
#comparação das empresas Brasil X Estados Unidos em um histograma
ax4.hist(brasil_empresas, bins=separações, weights=pesos_brasil,
         alpha=0.7,label="Brazil",color="#6cc47c",edgecolor="black")

ax4.hist(Estados_Unidos_empresas,bins=separações,weights=pesos_Estados_Unidos, alpha=0.5, 
         label="Estados Unidos",color="#0394fc",edgecolor="black")

ax4.legend( fontsize= 'small', bbox_to_anchor=(0.6, -0.3, 0.1, 0.1) )
ax4.set_title("Distribuição proporcional das empresas\npor nota Brasil x Estados Unidos", fontsize=7.5)
ax4.tick_params(axis="y", labelsize=8)
ax4.tick_params(axis="x", labelsize=8)
ax4.set_xlim(1, 5)
ax4.yaxis.set_major_formatter(PercentFormatter(1.0)) 






