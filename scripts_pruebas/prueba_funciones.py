from sorteo import sorteoNumeros, sorteoLotes, sorteoOrdenPrelacion
import pandas as pd
from pandas._testing import assert_frame_equal

# ----- Creación del DataFrame de los participantes -----
df_participantes = pd.read_csv('./datos/PARTICIPANTES SORTEO 13 LOTES UNISON.csv')
df_participantes.columns = ['num_empleado', 'antiguedad', '']
df_participantes = df_participantes[['num_empleado', 'antiguedad']]
df_participantes = df_participantes.sort_values(by=['antiguedad'], ascending=[False])


# ----- Creación del DataFrame de los terrenos -----
df_lotes = pd.read_csv('./datos/LOTES.csv')

# Semillas
semilla_asignacion_numeros = "08/08/2021 14:01"
semilla_asignacion_ganadores = "08/08/2021 14:30"
semilla_asignacion_orden_prelacion = "08/08/2021 15:08"

# Sorteo de los números, lotes y orden de prelación
df_sorteo_numeros, pila_numeros_mezclados = sorteoNumeros(df_participantes, semilla_asignacion_numeros)
df_sorteo_lotes = sorteoLotes(semilla_asignacion_ganadores, df_sorteo_numeros, df_lotes, pila_numeros_mezclados)

lista_participantes_totales = list(df_sorteo_numeros['num_empleado'])
lista_participantes_ganadores = list(df_sorteo_lotes['num_empleado'])
df_sorteo_orden_prelacion = sorteoOrdenPrelacion(semilla_asignacion_orden_prelacion, lista_participantes_totales, lista_participantes_ganadores)


# Se guardan los resultados en un csv y se leen para simular lo que pasa en la realidad
df_sorteo_numeros.to_csv("sorteo_numeros.csv", index=False)
df_sorteo_numeros = pd.read_csv('sorteo_numeros.csv')

df_sorteo_lotes['numero_ganador'] = [f"\'{b}\'" for b in df_sorteo_lotes['numero_ganador']]
df_sorteo_lotes = df_sorteo_lotes.drop(columns=['antiguedad', 'numeros'])
df_sorteo_lotes.to_csv("sorteo_lotes.csv", index=False)
df_sorteo_lotes = pd.read_csv("sorteo_lotes.csv")
df_sorteo_lotes['Numero_Lote'] = df_sorteo_lotes['Numero_Lote'].astype('int64')

df_sorteo_orden_prelacion.to_csv('sorteo_orden_prelacion.csv', index=False)
df_sorteo_orden_prelacion = pd.read_csv('sorteo_orden_prelacion.csv')


# Se leen los archivos generados por la aplicación
df_sorteo_numeros_app = pd.read_csv('./semillas3/ASIGNACION_DE_NUMEROS_3.csv', skiprows=3)
df_sorteo_lotes_app = pd.read_csv('./semillas3/RESULTADOS_DEL_SORTEO_3.csv', skiprows=3)
df_sorteo_orden_prelacion_app = pd.read_csv('./semillas3/ORDEN_DE_PRELACION_3.csv', skiprows=3) 

assert_frame_equal(df_sorteo_numeros, df_sorteo_numeros_app)
assert_frame_equal(df_sorteo_lotes, df_sorteo_lotes_app)
assert_frame_equal(df_sorteo_orden_prelacion, df_sorteo_orden_prelacion_app)






