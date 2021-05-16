"""
    Este script realiza el sorteo aleatorio de 13 terrenos entre 144 trabajadores.
"""

import random # Para las selecciones aleatorias
import pandas as pd # Para el manejo de los datos

def sorteoBoletos(participantes, semilla):
    random.seed(semilla)

    # ----- GENERACIÓN DE LOS BOLETOS -----
    # Obtenemos el número total de boletos
    total_boletos = participantes['antiguedad'].sum()

    # Se generan con el formato 001, 002, ..., 010, 011, ..., 099, 100, 101...
    # Se calcula cuántos ceros necesitaremos
    n_ceros = len(str(total_boletos+1))
    boletos = [str(i).zfill(n_ceros) for i in range(1, total_boletos+1)]

    # Se desordenan aleatoriamente 10 veces
    for _ in range(0, 10):
        random.shuffle(boletos)

    # ----- ASIGNACIÓN ALEATORIA DE LOS BOLETOS A CADA PARTICIPANTE -----
    # Obtenemos las antiguedades de cada participante
    antiguedades = participantes['antiguedad']

    # Lista en donde se guardará la selección de boletos para cada participante
    # y que posteriormente se añadirá al DataFrame
    boletos_df = []

    # Generamos una copia de la lista de boletos desordenada
    boletos_copia = [boleto for boleto in boletos]

    for n_antiguedad in antiguedades:
        # Se toman aleatoriamente el número de boletos correspondiente al participante actual
        seleccion_boletos = random.sample(boletos_copia, n_antiguedad)
        boletos_df.append(seleccion_boletos)
        
        # Se eliminan los boletos seleccionados
        boletos_copia = [boleto for boleto in boletos_copia if boleto not in seleccion_boletos]

    # Se añade la columna de "boletos" al dataframe de participantes
    participantes['boletos'] = boletos_df
    
    return participantes, boletos

def sorteoTerrenos(semilla, participantes, terrenos, boletos_mezclados):
    random.seed(semilla)

    # Lista para almacenar los boletos ganadores de cada terreno
    boletos_ganadores = []

    # Lista para almacenar a los participantes gandores de cada terreno
    num_empleados_ganadores = []

    # Creamos una copia de los boletos
    boletos_copia = [boleto for boleto in boletos_mezclados]

    for terreno in terrenos['Numero_Lote'].values:    
        # Se selecciona un boleto aleatoriamente y se añade a la lista de boletos ganadores
        boleto_ganador = random.choice(boletos_copia)
        boletos_ganadores.append(boleto_ganador)
        
        # Se busca el boleto ganador en la lista de boletos del DataFrame 'participantes'.
        registro_ganador = participantes[participantes['boletos'].apply(lambda x: boleto_ganador in x)]
        
        # Extraemos el número de trabajador del participante ganador y lo añadimos a la lista
        num_empleados_ganadores.append(registro_ganador['num_empleado'].values[0])
        
        # Extraemos la lista de los boletos del ganador
        boletos_a_eliminar = registro_ganador['boletos'].values[0]
        
        # Eliminamos todos los boletos del ganador de los boletos disponibles
        boletos_copia = [boleto for boleto in boletos_copia if boleto not in boletos_a_eliminar]

    # Añadimos al DataFrame de los terrenos a los ganadores
    terrenos['boleto_ganador'] = boletos_ganadores
    terrenos['num_empleado'] = num_empleados_ganadores

    # Combinamos el dataframe de los terrenos con el de los participantes
    # y lo guardamos en un archivo
    resultados = pd.merge(terrenos, participantes, on="num_empleado", how="outer")
    resultados = resultados.head(len(terrenos.index))
    return resultados



if __name__ == '__main__':
    # Información para crear la semilla.
    dia = 10
    mes = 11
    anio = 2021
    hora = 10
    minuto = 25
    segundo = 27

    random.seed(f"{dia}/{mes}/{anio} {hora}:{minuto}:{segundo}")

    # ----- LECTURA DEL ARCHIVO DE LOS PARTICIPANTES -----
    # Se lee el archivo csv de los participantes y se ordena de mayor a menor de acuerdo a la antigüedad
    participantes = pd.read_csv('datos/participantes.csv').sort_values(by=['antiguedad'], 
                                                                    ascending=False)
    participantes.reset_index(drop=True, inplace=True)

    # Nos aseguramos de que existan 144 números de empleado únicos y 144 nombres únicos
    n_num_empleados_unicos = len(pd.unique(participantes['num_empleado']))
    n_nombres_unicos = len(pd.unique(participantes['nombre']))

    if n_num_empleados_unicos != 144 or n_nombres_unicos != 144:
        raise AssertionError("Algún número de empleado o nombre se repite")

    # ----- LECTURA DEL ARCHIVO DE LOS TERRENOS -----
    terrenos = pd.read_csv('datos/terrenos.csv')

    # ----- GENERACIÓN DE LOS BOLETOS -----
    # Obtenemos el número total de boletos
    total_boletos = participantes['antiguedad'].sum()

    # Se generan con el formato 001, 002, ..., 010, 011, ..., 099, 100, 101...
    boletos = [str(i).zfill(3) for i in range(1, total_boletos+1)]

    # Se desordenan aleatoriamente 10 veces
    for _ in range(0, 10):
        random.shuffle(boletos)

    # ----- ASIGNACIÓN ALEATORIA DE LOS BOLETOS A CADA PARTICIPANTE -----
    # Obtenemos las antiguedades de cada participante
    antiguedades = participantes['antiguedad']

    # Lista en donde se guardará la selección de boletos para cada participante
    # y que posteriormente se añadirá al DataFrame
    boletos_df = []

    # Generamos una copia de la lista de boletos desordenada
    boletos_copia = [boleto for boleto in boletos]

    for n_antiguedad in antiguedades:
        # Se toman aleatoriamente el número de boletos correspondiente al participante actual
        seleccion_boletos = random.sample(boletos_copia, n_antiguedad)
        boletos_df.append(seleccion_boletos)
        
        # Se eliminan los boletos seleccionados
        boletos_copia = [boleto for boleto in boletos_copia if boleto not in seleccion_boletos]

    # Se añade la columna de "boletos" al dataframe de participantes
    participantes['boletos'] = boletos_df

    # ----- VALIDACIÓN DE LA SELECCIÓN DE BOLETOS -----

    # Revisión para asegurar que cada boleto le corresponde únicamente a un solo participante

    # Obtenemos la columna "boletos"
    columna_boletos = [list(l) for l in participantes['boletos'].values]

    for i in range(144):
        # Tomamos la lista [0]
        lista_actual = columna_boletos.pop(0)
        # Comparamos cada boleto en la lista actual con los
        # boletos que se encuentran en las demás listas de boletos
        for boleto in lista_actual:
            for lista_restante in columna_boletos:
                if boleto in lista_restante:
                    raise AssertionError(f"El boleto {boleto} se repite")
        
        # Se añade la lista tomada hasta el final de la columna.
        columna_boletos.append(lista_actual)

    # Revisión para asegurar que el número de boletos elegidos para cada participante corresponda con
    # sus años de antigüedad
    for registro in participantes.iterrows():
        # Checamos que la antigüedad coincida con la longitud de su lista de boletos
        if registro[1]['antiguedad'] != len(registro[1]['boletos']):
            raise AssertionError(f"La antigüedad del trabajador {registro[1]['num_empleado']} no " + 
                                "coincide con el número de boletos que se le han asignado.")


    # ----- SELECCIÓN DE LOS GANADORES -----   
    # Lista para almacenar los boletos ganadores de cada terreno
    boletos_ganadores = []

    # Lista para almacenar a los participantes gandores de cada terreno
    num_empleados_ganadores = []

    # Creamos una copia de los boletos
    boletos_copia = [boleto for boleto in boletos]

    for terreno in terrenos['terreno'].values:    
        # Se selecciona un boleto aleatoriamente y se añade a la lista de boletos ganadores
        boleto_ganador = random.choice(boletos_copia)
        boletos_ganadores.append(boleto_ganador)
        
        # Se busca el boleto ganador en la lista de boletos del DataFrame 'participantes'.
        registro_ganador = participantes[participantes['boletos'].apply(lambda x: boleto_ganador in x)]
        
        # Extraemos el número de trabajador del participante ganador y lo añadimos a la lista
        num_empleados_ganadores.append(registro_ganador['num_empleado'].values[0])
        
        # Extraemos la lista de los boletos del ganador
        boletos_a_eliminar = registro_ganador['boletos'].values[0]
        
        # Eliminamos todos los boletos del ganador de los boletos disponibles
        boletos_copia = [boleto for boleto in boletos_copia if boleto not in boletos_a_eliminar]

    # Añadimos al DataFrame de los terrenos a los ganadores
    terrenos['boleto_ganador'] = boletos_ganadores
    terrenos['num_empleado'] = num_empleados_ganadores

    # Combinamos el dataframe de los terrenos con el de los participantes
    # y lo guardamos en un archivo
    resultados = pd.merge(terrenos, participantes, on="num_empleado", how="outer")
    resultados = resultados.fillna('-')
    resultados.reset_index(drop=True, inplace=True)
    resultados.to_csv("datos/resultados.csv", index=False)