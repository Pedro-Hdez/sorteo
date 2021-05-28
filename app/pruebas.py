import pandas as pd
from sorteo import *

df_participantes = pd.read_csv('./datos/PARTICIPANTES SORTEO 13 LOTES UNISON.csv')
df_participantes.columns = ['num_empleado', 'antiguedad', '']
df_participantes = df_participantes[['num_empleado', 'antiguedad']]
df_participantes = df_participantes.sort_values(by=['antiguedad'], ascending=[False])

df_terrenos = pd.read_csv('./datos/LOTES.csv')

participantes, numeros = sorteoNumeros(df_participantes, 1)

print("SORTEO DE NÚMEROS")
print(participantes.head(20))

sorteoLotes(1, participantes, df_terrenos, numeros)

