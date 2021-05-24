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
                         ['num_empleado', 'antiguedad', 'boletos].
        
        -boletos: Objeto <list> que contiene la lista de boletos desordenados que se han sorteado.
    """

    # Se establece la semilla
    random.seed(semilla)

    # ----- GENERACIÓN DE LOS BOLETOS -----

    # Obtenemos el número total de boletos
    total_boletos = participantes['antiguedad'].sum()

    # Se generan con el formato 0001, 0002, ..., 0010, 0011, ..., 0099, 0100, 0101..., 0999, 1000,...
    # Primero, se calcula el número de ceros que necesitamos de acuerdo al número
    # de dígitos que tenga el número total de boletos
    n_ceros = len(str(total_boletos))
    boletos = [str(i).zfill(n_ceros) for i in range(1, total_boletos+1)]

    # ----- MEZCLA DE LOS BOLETOS -----

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
    """
        Esta función realiza el sorteo aleatorio de los terrenos.

        Parámetros
        ----------
        - semilla: Objeto <str> que se utilizará como semilla para los procesos aleatorios
                   proporcionados por la librería 'random'.

        - participantes: Objeto pd.DataFrame que contien las columnas 
                         ['num_empleado', 'antiguedad', 'boletos'].
        
        - terrenos: Objeto pd.DataFrame que contien la columna ['Numero_Lote'].

        - boletos_mezclados: Objeto <list> que contiene la lista de boletos desordenados que se han 
                             sorteado.
        
        Regresa
        -------
        - resultados: Objeto pd.DataFrame que contiene a los ganadores de los terrenos. Cuenta con
                      las columnas ['Numero_Lote', 'boleto_ganador', 'num_empleado', 
                                    'antiguedad', 'boletos']
    """

    # Se establece la semilla
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
    resultados = pd.merge(terrenos, participantes, on="num_empleado", how="outer")
    resultados = resultados.head(len(terrenos.index))
    
    return resultados