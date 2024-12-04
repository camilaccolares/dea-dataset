import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydea
from itertools import combinations
from datetime import datetime

begin = datetime.now()

#carregando dataset com fatores
inputs_fixos = pd.read_excel('inputs_fixos.xlsx')
outputs_fixos = pd.read_excel('outputs_fixos.xlsx')
fatores_candidatos = pd.read_excel('fatores_candidatos.xlsx')

#criando lista com nomes de fatores 
fatores_lista = list(fatores_candidatos.columns)

#gerando as combinacoes 4 a 4
comb = list(combinations(fatores_lista, 4))

#dataframe que ira armazenar o melhor resultado
melhor_resultado = pd.DataFrame()

#lista que ira armazenar os fatores do melhor resultado
melhores_fatores = []

cont = 0
for i in comb:
    #cont = cont + 1
    #print(f'EXECUCAO N {cont}')
    #if cont == 101:
    #    break
    inputs = pd.DataFrame()
    outputs = pd.DataFrame()
    resultado_candidato = pd.DataFrame()
    inputs = inputs_fixos
    outputs = outputs_fixos
    for j in i:
        coluna = fatores_candidatos[j]
        if 'input' in j: 
            inputs = inputs.join(coluna)
        else:
            outputs = outputs.join(coluna)
    problema = pydea.DEAProblem(inputs, outputs, returns='CRS')
    resultado = problema.solve()
    resultado_candidato['eficiencia'] = resultado['Efficiency']
    if len(melhores_fatores) == 0: #se for a primeira execucao, popula as variaveis
        melhor_resultado['eficiencia'] = resultado_candidato['eficiencia']
        melhores_fatores = list(inputs.columns) + list(outputs.columns)
    else: #se nao, compara o resultado atual com o melhor resultado e substitui se for o caso
        soma_candidato = resultado_candidato['eficiencia'].sum()
        soma_melhor = melhor_resultado['eficiencia'].sum()
        if soma_candidato > soma_melhor: #se o resultado atual for melhor, substitui
            melhor_resultado['eficiencia'] = resultado_candidato['eficiencia']
            melhores_fatores = list(inputs.columns) + list(outputs.columns)
end = datetime.now()

begin_time = begin.strftime("%H:%M:%S")
end_time = end.strftime("%H:%M:%S")
k = melhor_resultado['eficiencia'].sum()

with open('resultados.txt', 'w') as f:
    f.write("Inicio: ")
    f.write(begin_time)
    f.write("\n")
    f.write("Termino: ")
    f.write(end_time)
    f.write("\n")
    f.write("Soma melhor resultado: ")
    f.write(str(k))
    f.write("\n")
    f.write("Eficiencias:")
    f.write("\n")
    f.write(str(melhor_resultado['eficiencia']))
    f.write("\n")
    f.write("Fatores:")
    f.write("\n")
    f.write(str(melhores_fatores))