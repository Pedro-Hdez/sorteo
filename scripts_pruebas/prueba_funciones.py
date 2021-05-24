from pandas.io.parsers import read_csv
from sorteo import sorteoTerrenos, sorteoBoletos
import pandas as pd
from pandas._testing import assert_frame_equal

# ----- Creación del DataFrame de los participantes -----
df_participantes = pd.read_csv('./datos/PARTICIPANTES SORTEO 13 LOTES UNISON.csv')
df_participantes.columns = ['num_empleado', 'antiguedad', '']
df_participantes = df_participantes[['num_empleado', 'antiguedad']]
df_participantes = df_participantes.sort_values(by=['antiguedad'], ascending=[False])


# ----- Creación del DataFrame de los terrenos -----
df_terrenos = pd.read_csv('./datos/terrenos.csv')

# Sorteo de los boletos y terrenos
df_sorteo_boletos, pila_boletos_mezclados = sorteoBoletos(df_participantes, "20/05/2021 00:44")
df_sorteo_terrenos = sorteoTerrenos("20/05/2021 00:45", df_sorteo_boletos, df_terrenos, pila_boletos_mezclados)

df_sorteo_boletos.to_csv("sorteo_boletos.csv", index=False)
df_sorteo_boletos = read_csv('sorteo_boletos.csv')

df_sorteo_terrenos['boleto_ganador'] = [f"\'{b}\'" for b in df_sorteo_terrenos['boleto_ganador']]
df_sorteo_terrenos = df_sorteo_terrenos.drop(columns=['antiguedad', 'boletos'])
df_sorteo_terrenos.to_csv("sorteo_terrenos.csv", index=False)
df_sorteo_terrenos = pd.read_csv("sorteo_terrenos.csv")
df_sorteo_terrenos['Numero_Lote'] = df_sorteo_terrenos['Numero_Lote'].astype('int64')

df_sorteo_boletos_original = pd.read_csv('./corrida_2/ASIGNACION_DE_BOLETOS_3.csv', skiprows=3)
df_sorteo_terrenos_original = pd.read_csv('./corrida_2/RESULTADOS_DEL_SORTEO_3.csv', skiprows=3)

assert_frame_equal(df_sorteo_boletos, df_sorteo_boletos_original)
assert_frame_equal(df_sorteo_terrenos, df_sorteo_terrenos_original)






