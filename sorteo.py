"""
    Este script contiene las funciones para sortear los boletos y sortear
    los terrenos.
"""
import random # Para los procedimientos aleatorios
import pandas as pd # Para el manejo de los datos

def sorteoBoletos(participantes, semilla):
    """
        Esta función realiza el sorteo aleatorio de boletos entre todos
        los participantes. El número de boletos es igual a la sumatoria de las antigüedades de los
        participantes.

        Parámetros
        ----------
        - participantes: Objeto pd.DataFrame que contien las columnas ['num_empleado', 'antiguedad'].
        
        - semilla: Objeto <str> que se utilizará como semilla para los procesos aleatorios
                   proporcionados por la librería 'random'.
        
        Regresa
        -------
        - participantes: Objeto pd.DataFrame que contiene la asignación de los boletos para cada
                         participante. Cuenta con las columnas  
                         ['num_empleado', 'antiguedad', 'numeros'].
        
        - numeros: Objeto <list> que contiene la lista de números desordenados que se han asignado.
    """

    # Se establece la semilla
    random.seed(semilla)

    # ----- GENERACIÓN DE LOS NÚMEROS -----

    # Obtenemos el número total de boletos
    total_numeros = participantes['antiguedad'].sum()

    # Se generan con el formato 0001, 0002, ..., 0010, 0011, ..., 0099, 0100, 0101..., 0999, 1000,...
    # Primero, se calcula la cantidad de ceros que necesitamos de acuerdo a la cantidad
    # de dígitos que tenga el número total de boletos
    n_ceros = len(str(total_numeros))
    numeros = [str(i).zfill(n_ceros) for i in range(1, total_numeros+1)]

    # ----- MEZCLA DE LOS NÚMERO -----

    # Los números se mezclan aleatoriamente 10,000 veces
    for _ in range(0, 10000):
        random.shuffle(numeros)

    # ----- ASIGNACIÓN ALEATORIA DE LOS NÚMEROSS A CADA PARTICIPANTE -----

    # Obtenemos las antiguedades de cada participante
    antiguedades = participantes['antiguedad']

    # Lista en donde se guardará la selección de números para cada participante
    # y que posteriormente se añadirá al DataFrame 'participantes'
    numeros_df = []

    # Generamos una copia de la lista de números desordenada
    numeros_copia = [numero for numero in numeros]

    # Se recorre la lista de antiguedades para asignar la respectiva cantidad de números
    for n_antiguedad in antiguedades:
        # Se toman aleatoriamente el número de boletos correspondiente al participante actual
        seleccion_numeros = random.sample(numeros_copia, n_antiguedad)
        numeros_df.append(seleccion_numeros)
        
        # Se eliminan los boletos seleccionados de la pila de números
        numeros_copia = [numero for numero in numeros_copia if numero not in seleccion_numeros]

    # Se añade la columna de "numeros" al dataframe de participantes
    participantes['numeros'] = numeros_df
    
    return participantes, numeros

def sorteoLotes(semilla, participantes, terrenos, numeros_mezclados):
    """
        Esta función realiza el sorteo aleatorio de los terrenos.

        Parámetros
        ----------
        - semilla: Objeto <str> que se utilizará como semilla para los procesos aleatorios
                   proporcionados por la librería 'random'.

        - participantes: Objeto pd.DataFrame que contien las columnas 
                         ['num_empleado', 'antiguedad', 'numeros'].
        
        - terrenos: Objeto pd.DataFrame que contien la columna ['Numero_Lote'].

        - numeros_mezclados: Objeto <list> que contiene la lista de números desordenados que se han 
                             asignado.
        
        Regresa
        -------
        - resultados: Objeto pd.DataFrame que contiene a los ganadores de los terrenos. Cuenta con
                      las columnas ['Numero_Lote', 'numero_ganador', 'num_empleado', 
                                    'antiguedad', 'numeros']
    """

    # Se establece la semilla
    random.seed(semilla)

    # Lista para almacenar los números ganadores de cada terreno
    numeros_ganadores = []

    # Lista para almacenar los números de empleado de los participantes gandores
    num_empleados_ganadores = []

    # Creamos una copia de los números mezclados
    numeros_copia = [numero for numero in numeros_mezclados]

    # Se recorren los terrenos para asignar un ganador a cada uno
    for terreno in terrenos['Numero_Lote'].values:    
        # Se selecciona el número ganado aleatoriamente y se añade a la lista de números ganadores
        numero_ganador = random.choice(numeros_copia)
        numeros_ganadores.append(numero_ganador)
        
        # Se busca el número ganador en la lista de boletos del DataFrame 'participantes'.
        registro_ganador = participantes[participantes['numeros'].apply(lambda x: numero_ganador in x)]
        
        # Extraemos el número de trabajador del participante ganador y lo añadimos a la lista de 
        # números de empleado de participantes ganadores
        num_empleados_ganadores.append(registro_ganador['num_empleado'].values[0])
        
        # Extraemos la lista de los números del participante ganador
        numeros_a_eliminar = registro_ganador['numeros'].values[0]
        
        # Eliminamos todos los números pertenecientes al participante ganador 
        # de la pila de números disponibles
        numeros_copia = [numero for numero in numeros_copia if numero not in numeros_a_eliminar]

    # Añadimos al DataFrame de los terrenos los datos de los ganadores
    terrenos['numero_ganador'] = numeros_ganadores
    terrenos['num_empleado'] = num_empleados_ganadores

    # Combinamos el dataframe de los terrenos con el de los participantes
    resultados = pd.merge(terrenos, participantes, on="num_empleado", how="outer")
    resultados = resultados.head(len(terrenos.index))
    
    return resultados