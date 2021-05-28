import os
import pandas as pd
from pandas._testing import assert_frame_equal

def checarUnicidadBoletos(df):
    # Obtenemos las listas de numeros de cada participante
    columna_numeros = [l[1:-1].split(', ') for l in df['numeros'].values]

    # Checamos lista por lista
    for i in range(len(columna_numeros)):
        # Sacamos la lista[0]
        lista_actual = columna_numeros.pop(0)
        # Comparamos cada boleto en la lista actual con los
        # numeros que se encuentran en las demás listas de numeros
        for boleto in lista_actual:
            for lista_restante in columna_numeros:
                # Si el boleto actual se encuentra en alguna otra lista de numeros,
                # entonces se dispara un error.
                if boleto in lista_restante:
                    raise AssertionError(f"El boleto {boleto} se repite")
        
        # Cuando hayamos validado la lista actual, entonces la volvemos a meter a 
        # la lista de listas de los numeros, pero hasta el final. De este modo
        # las siguentes validaciones también tomarán en cuenta a esta lista.
        columna_numeros.append(lista_actual)
    
    # Si se revisaron todos los numeros de todas las listas, entonces se despliega
    # un mensaje de éxito.
    print(f"La unicidad de los numeros se ha validado con éxito")

def checarNumeroDeBoletosAsignados(df):
    for registro in df.iterrows():
        lista_numeros = registro[1]['numeros'][1:-1].split(', ')
        # Checamos que la antigüedad coincida con la longitud de su lista de numeros
        if registro[1]['antiguedad'] != len(lista_numeros):
            # Si la antiguedad no coincide con el número de numeros asignados, se
            # dispara un error.
            raise AssertionError(f"La antigüedad del trabajador {registro[1]['num_empleado']} no coincide con el número de numeros que se le han asignado.")
    
    # Si se revisaron el número de numeros de todos los participantes, entonces se 
    # despliega un mensaje de éxito
    print(f"A todos los participantes se le han asignado el número correcto de numeros")

def checarUnicidadGanadores(df):
    if (len(pd.unique(df['numero_ganador']))) != len(df.index):
        raise AssertionError('Se repite un boleto ganador')
    
    if (len(pd.unique(df['num_empleado']))) != len(df.index): 
        raise AssertionError('Un participante ganó más de una vez')
    
    print("Los numeros ganadores y los números de empleado ganadores son únicos.")


def checarCorrespondenciaBoletoGanador(df_numeros, df_ganadores):
    for i in range(len(df_ganadores.index)):
        terreno_actual = df_ganadores.iloc[i]
        numero_ganador = terreno_actual['numero_ganador']
        participante_ganador = terreno_actual['num_empleado']

        registro_participante_ganador = df_numeros[df_numeros['num_empleado'] == participante_ganador]
        numeros_participante_ganador = [l[1:-1].split(', ') for l in registro_participante_ganador['numeros'].values][0]

        if numero_ganador not in numeros_participante_ganador:
            raise AssertionError(f'El boleto ganador {numero_ganador} no pertenece al ganador {participante_ganador}')

        if participante_ganador != registro_participante_ganador['num_empleado'].values[0]:
            raise AssertionError(f'El ganador reportado es diferente al poseedor del boleto ganador')
    
    print("La correspondencia de los numeros ganadores con sus dueños se ha verificado con éxito.")


def checarIdentidadDataFrames(df1, df2):
    try:
        assert_frame_equal(df1, df2)
        print(f"Los dataframes son iguales")
    except:
        raise AssertionError(f'Los dataFrames son diferentes')


def checarQueTodosLosParticipantesRecibieronBoletos(df_participantes, df_asignacion_numeros):
    participantes_originales = list(df_participantes['num_empleado'])
    participantes_con_boleto = list(df_asignacion_numeros['num_empleado'])
    faltantes = [p for p in participantes_originales if p not in participantes_con_boleto]
    if faltantes:
        raise AssertionError(f'Los empleados {faltantes} no aparecen en la asignación de boletos')
    print("Todos los participantes tienen boletos asignados")

def checarQueLosParticipantesNoSeRepitenEnLaAsignacionDeBoletos(df_participantes, df_asignacion_numeros):
    n_participantes = len(df_participantes.index)
    n_participantes_con_boletos = len(pd.unique(df_asignacion_numeros['num_empleado']))

    if n_participantes != n_participantes_con_boletos:
        raise AssertionError("A ALGÚN PARTICIÁNTE SE LE ASIGNARON BOLETOS MÁS DE UNA VEZ")
    print("Los participantes no se repiten en el DataFrame de asignación de boletos")

def checarQueLosNumerosNoSeRepitenEnElMismoParticipante(df):
    # Obtenemos las listas de numeros de cada participante
    columna_numeros = [l[1:-1].split(', ') for l in df['numeros'].values]

    # Checamos lista por lista
    for lista in columna_numeros:
        # Checamos boleto por boleto en la lista actual
        if any(lista.count(numero) > 1 for numero in lista):
            raise AssertionError("SE REPITE ALGÚN BOLETO DENTRO DE LA LISTA DE UN PARTICIPANTE")
    
    print("Cada participante tiene su cantidad correspondiente de boletos únicos")

def checarQueCadaParticipanteTengaSuCorrespondienteAntiguedad(df_participantes, df_asignacion_numeros):
    
    # Se ordena el DataFrame de los participantes originales de acuerdo a su antiguedad y luego por num_empleado
    df_participantes_ordenados = df_participantes.sort_values(by=['antiguedad', 'num_empleado'], ascending=[False, False])
    # Se resetea el índice
    df_participantes_ordenados = df_participantes_ordenados.reset_index(drop=True)

    # Se ordena el DataFrame de la asignacion de número de acuerdo a la antiguedad y luego por num_empleado
    df_asignacion_numeros_ordenados = df_asignacion_numeros.sort_values(by=['antiguedad', 'num_empleado'], ascending=[False, False])
    # Se elimina la columna de boletos del Dataframe de la asignación de números
    df_asignacion_numeros_ordenados = df_asignacion_numeros_ordenados[['num_empleado', 'antiguedad']]
    # Se resetea el índice
    df_asignacion_numeros_ordenados = df_asignacion_numeros_ordenados.reset_index(drop=True)

    try:
        assert_frame_equal(df_participantes_ordenados, df_asignacion_numeros_ordenados)
        print(f"Los dataframes son iguales")
    except:
        raise AssertionError(f'Los dataFrames son diferentes')

def checarQueElBoletoGanadorNoSeRepita(df_resultados, df_terrenos):
    n_terrenos = len(df_terrenos.index)
    if len(pd.unique(df_resultados['numero_ganador'])) != n_terrenos:
        raise AssertionError(f'UN BOLETO GANADOR SE REPITE')
    
    print("Los boletos ganadores no se repiten")

def checarQueNingunGanadorExistaEnElOrdenDePrelacion(df_ganadores, df_orden_prelacion):
    lista_participantes_ganadores = list(df_ganadores['num_empleado'])
    lista_participantes_no_ganadores = list(df_orden_prelacion['num_empleado'])

    # Se checa que ningún ganador exista en la orden de prelación
    for ganador in lista_participantes_ganadores:
        if ganador in lista_participantes_no_ganadores:
            raise AssertionError(f'EL PARTICIPANTE GANADOR {ganador} SE REPITE EN LOS GANADORES Y EN LA ORDEN DE PRELACION')
    
    # Se checa que ningún no ganador exista en la lista de ganadores
    for no_ganador in lista_participantes_no_ganadores:
        if no_ganador in lista_participantes_ganadores:
            raise AssertionError(f'EL PARTICIPANTE NO GANADOR {no_ganador} SE REPITE EN LA ORDEN DE PRELACIÓN Y EN  LA LISTA DE GANADORES')
    
    print("Ningún ganador se encuentra en la orden de prelación; y ningún NO ganador se encuentra en la lista de ganadores")

def checarQueNingunParticipanteSeRepitaEnLaOrdenDePrelacion(df_orden_prelacion):
    if (len(pd.unique(df_orden_prelacion['num_empleado']))) != len(df_orden_prelacion.index):
        raise AssertionError(f'ALGÚN PARTICIPANTE SE REPITE EN LA ORDEN DE PRELACIÓN')
    print("Ningún participante se repite en la orden de prelación")

def checarQueLaSumaDeLosGanadoresYNoGanadoresSeaIgualAlTotal(df_participantes, df_orden_prelacion, df_ganadores):
    if len(df_orden_prelacion.index) + len(df_ganadores.index)  != len(df_participantes.index):
        raise AssertionError(f'LA SUMA DEL NÚMERO DE GANADORES Y EL NÚMERO DE NO GANADORES ES DIFERENTE DEL NÚMERO TOTAL DE PARTICIPANTES ({len(df_participantes.index)})')
    print("La suma de los ganadores y no ganadores es igual al número total de participantes")

def checarQueUnionDeGanadoresYNoGanadoresEsIgualALaListaDeParticipantesOriginal(df_participantes, df_orden_prelacion, df_ganadores):
    participantes_originales  = list(df_participantes['num_empleado'])
    participantes_ganadores = list(df_ganadores['num_empleado']) 
    participantes_no_ganadores = list(df_orden_prelacion['num_empleado'])

    union = participantes_ganadores + participantes_no_ganadores
    participantes_originales.sort()
    union.sort()

    if union != participantes_originales:
        raise AssertionError(f'LA UNIÓN DE GANADORES Y NO GANADORES ES DIFERENTE A LA LISTA DE PARTICIPANTES ORIGINAL')
    print("La unión de ganadores y no ganadores es igual a la lista de participantes original")



# ----- Creación del DataFrame de los participantes -----
df_participantes = pd.read_csv('./datos/PARTICIPANTES SORTEO 13 LOTES UNISON.csv')
df_participantes.columns = ['num_empleado', 'antiguedad', '']
df_participantes = df_participantes[['num_empleado', 'antiguedad']]
df_participantes = df_participantes.sort_values(by=['antiguedad'], ascending=[False])


# ----- Creación del DataFrame de los terrenos -----
df_lotes = pd.read_csv('./datos/LOTES.csv')

root = "./"
for f in os.listdir(root):
    folder = root+f
    if os.path.isdir(folder) and folder != "./datos":
        print(f"***** REVISANDO LAS CORRIDAS DE: {folder} *****")

        archivo_numeros_1 = folder+"/ASIGNACION_DE_NUMEROS_1.csv"
        archivo_numeros_2 = folder+"/ASIGNACION_DE_NUMEROS_2.csv"
        archivo_numeros_3 = folder+"/ASIGNACION_DE_NUMEROS_3.csv"

        archivo_terrenos_1 = folder+"/RESULTADOS_DEL_SORTEO_1.csv"
        archivo_terrenos_2 = folder+"/RESULTADOS_DEL_SORTEO_2.csv"
        archivo_terrenos_3 = folder+"/RESULTADOS_DEL_SORTEO_3.csv"

        archivo_orden_prelacion_1 = folder+"/ORDEN_DE_PRELACION_1.csv"
        archivo_orden_prelacion_2 = folder+"/ORDEN_DE_PRELACION_2.csv"
        archivo_orden_prelacion_3 = folder+"/ORDEN_DE_PRELACION_3.csv"

        # Se obtienen los csv de la asignación de numeros
        numeros1 = pd.read_csv(archivo_numeros_1, skiprows=3)
        numeros2 = pd.read_csv(archivo_numeros_2, skiprows=3)
        numeros3 = pd.read_csv(archivo_numeros_3, skiprows=3)

        # Se obtienen los csv de la asignación de terrenos
        terrenos1 = pd.read_csv(archivo_terrenos_1, skiprows=3)
        terrenos2 = pd.read_csv(archivo_terrenos_2, skiprows=3)
        terrenos3 = pd.read_csv(archivo_terrenos_3, skiprows=3)

        # Se obtienen los csv de la orden de prelación
        prelacion1 = pd.read_csv(archivo_orden_prelacion_1, skiprows=3)
        prelacion2 = pd.read_csv(archivo_orden_prelacion_2, skiprows=3)
        prelacion3 = pd.read_csv(archivo_orden_prelacion_3, skiprows=3)


        # ***************************************** FASE 2 *****************************************

        # Checar que todos los participantes reciban boletos
        print(f"---------- VALIDACIÓN DE QUE TODOS LOS PARTICIPANTES TENGAN BOLETOS ----------")
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_1}")
        checarQueTodosLosParticipantesRecibieronBoletos(df_participantes, numeros1)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_2}")
        checarQueTodosLosParticipantesRecibieronBoletos(df_participantes, numeros2)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_3}")
        checarQueTodosLosParticipantesRecibieronBoletos(df_participantes, numeros3)

        # Checar que los participantes no se repiten en la asignación de boletos
        print(f"\n\n---------- VALIDACIÓN DE QUE LOS PARTICIPANTES NO SE REPITEN EN LA ASIGNACIÓN DE BOLETOS ----------")
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_1}")
        checarQueLosParticipantesNoSeRepitenEnLaAsignacionDeBoletos(df_participantes, numeros1)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_2}")
        checarQueLosParticipantesNoSeRepitenEnLaAsignacionDeBoletos(df_participantes, numeros2)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_3}")
        checarQueLosParticipantesNoSeRepitenEnLaAsignacionDeBoletos(df_participantes, numeros3)

        # Checar que los boletos no se repiten en la lista en la que están
        print(f"\n\n---------- VALIDACIÓN DE QUE LOS NÚMEROS DE UN PARTICIÁNTE NO SE REPITAN EN SU MISMA LISTA DE NÚMEROS  ----------")
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_1}")
        checarQueLosNumerosNoSeRepitenEnElMismoParticipante(numeros1)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_2}")
        checarQueLosNumerosNoSeRepitenEnElMismoParticipante(numeros2)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_3}")
        checarQueLosNumerosNoSeRepitenEnElMismoParticipante(numeros3)

        # Se checa la unicidad de los numeros en cada corrida
        print(f"\n\n---------- VALIDACIÓN DE LA UNICIDAD DE LOS NUMEROS ----------")
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_1}")
        checarUnicidadBoletos(numeros1)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_2}")
        checarUnicidadBoletos(numeros2)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_3}")
        checarUnicidadBoletos(numeros3)

        # Se checa que el número de numeros asignados a cada participante coincida
        # con sus años e antiguedad
        print(f"\n\n---------- VALIDACIÓN DEL NÚMERO DE NUMEROS ASIGNADOS A LOS PARTICIPANTES ----------")
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_1}")
        checarNumeroDeBoletosAsignados(numeros1)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_2}")
        checarNumeroDeBoletosAsignados(numeros2)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_3}")
        checarNumeroDeBoletosAsignados(numeros3)

        # Checar que cada participante tenga su correspondiente antiguedad
        print(f"\n\n---------- VALIDACIÓN DE QUE LOS PARTICIPANTES TENGAN SU CORRESPONDIENTE ANTIGUEDAD ----------")
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_1}")
        checarQueCadaParticipanteTengaSuCorrespondienteAntiguedad(df_participantes, numeros1)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_2}")
        checarQueCadaParticipanteTengaSuCorrespondienteAntiguedad(df_participantes, numeros2)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_numeros_3}")
        checarQueCadaParticipanteTengaSuCorrespondienteAntiguedad(df_participantes, numeros3)



        # ***************************************** FASE 3 *****************************************
        


        # Se checa la unicidad de los ganadores
        print(f"\n\n---------- VALIDACIÓN DE LA UNICIDAD DE LOS GANADORES ----------")
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_terrenos_1}")
        checarUnicidadGanadores(terrenos1)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_terrenos_2}")
        checarUnicidadGanadores(terrenos2)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_terrenos_3}")
        checarUnicidadGanadores(terrenos3)

        # Se checa la correspondencia de los numeros ganadores con sus dueños
        print(f"\n\n---------- VALIDACIÓN DE LA CORRESPONDENCIA DE LOS NUMEROS GANADORS CON SUS DUEÑOS ----------")
        print(f"\nVALIDANDO {archivo_numeros_1} y {archivo_terrenos_1}")
        checarCorrespondenciaBoletoGanador(numeros1, terrenos1)
        print(f"\nVALIDANDO {archivo_numeros_2} y {archivo_terrenos_2}")
        checarCorrespondenciaBoletoGanador(numeros2, terrenos2)
        print(f"\nVALIDANDO {archivo_numeros_3} y {archivo_terrenos_3}")
        checarCorrespondenciaBoletoGanador(numeros3, terrenos3)

        # Checar que el boleto ganador no se repita
        print(f"\n\n---------- VALIDACIÓN DE LA UNICIDAD DE LOS BOLETOS GANADORES ----------")
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_terrenos_1}")
        checarQueElBoletoGanadorNoSeRepita(terrenos1, df_lotes)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_terrenos_2}")
        checarQueElBoletoGanadorNoSeRepita(terrenos2, df_lotes)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_terrenos_3}")
        checarQueElBoletoGanadorNoSeRepita(terrenos3, df_lotes)


        # Se checa que los tres dataframes de numeros sean idénticos
        print(f"\n\n---------- VALIDACIÓN DE LA IDENTIDAD DE LOS DATAFRAMES DE ASIGNACIÓN DE NUMEROS ----------")
        print(f"\nVALIDANDO {archivo_numeros_1} y {archivo_numeros_2}")
        checarIdentidadDataFrames(numeros1, numeros2)
        print(f"\nVALIDANDO {archivo_numeros_1} y {archivo_numeros_3}")
        checarIdentidadDataFrames(numeros1, numeros3)
        print(f"\nVALIDANDO {archivo_numeros_2} y {archivo_numeros_3}")
        checarIdentidadDataFrames(numeros2, numeros3)

        # Se checa que los tres dataframes de terrenos
        print(f"\n\n---------- VALIDACIÓN DE LA IDENTIDAD DE LOS DATAFRAMES DE ASIGNACIÓN DE TERRENOS ----------")
        print(f"\nVALIDANDO {archivo_terrenos_1} y {archivo_terrenos_2}")
        checarIdentidadDataFrames(terrenos1, terrenos2)
        print(f"\nVALIDANDO {archivo_terrenos_1} y {archivo_terrenos_3}")
        checarIdentidadDataFrames(terrenos1, terrenos3)
        print(f"\nVALIDANDO {archivo_terrenos_2} y {archivo_terrenos_3}")
        checarIdentidadDataFrames(terrenos2, terrenos3)
        print(f"\n\n\n")


        # ***************************************** FASE 4 *****************************************1

        # Checar que ningún ganador exista en el orden de prelación
        print(f"\n\n---------- VALIDACIÓN DE QUE UN GANADOR NO SE ENCUENTRE EN LA ORDEN DE PRELACION Y VICEVERSA ----------")
        print(f"\nVALIDANDO {archivo_terrenos_1} y {archivo_orden_prelacion_1}")
        checarQueNingunGanadorExistaEnElOrdenDePrelacion(terrenos1, prelacion1)
        print(f"\nVALIDANDO {archivo_terrenos_1} y {archivo_orden_prelacion_2}")
        checarQueNingunGanadorExistaEnElOrdenDePrelacion(terrenos1, prelacion2)
        print(f"\nVALIDANDO {archivo_terrenos_1} y {archivo_orden_prelacion_3}")
        checarQueNingunGanadorExistaEnElOrdenDePrelacion(terrenos1, prelacion3)
        print(f"\nVALIDANDO {archivo_terrenos_2} y {archivo_orden_prelacion_1}")
        checarQueNingunGanadorExistaEnElOrdenDePrelacion(terrenos2, prelacion1)
        print(f"\nVALIDANDO {archivo_terrenos_2} y {archivo_orden_prelacion_2}")
        checarQueNingunGanadorExistaEnElOrdenDePrelacion(terrenos2, prelacion2)
        print(f"\nVALIDANDO {archivo_terrenos_2} y {archivo_orden_prelacion_3}")
        checarQueNingunGanadorExistaEnElOrdenDePrelacion(terrenos2, prelacion3)
        print(f"\nVALIDANDO {archivo_terrenos_3} y {archivo_orden_prelacion_1}")
        checarQueNingunGanadorExistaEnElOrdenDePrelacion(terrenos3, prelacion1)
        print(f"\nVALIDANDO {archivo_terrenos_3} y {archivo_orden_prelacion_2}")
        checarQueNingunGanadorExistaEnElOrdenDePrelacion(terrenos3, prelacion2)
        print(f"\nVALIDANDO {archivo_terrenos_3} y {archivo_orden_prelacion_3}")
        checarQueNingunGanadorExistaEnElOrdenDePrelacion(terrenos3, prelacion3)

        # Checar que ningún participante se repita en la orden de prelación
        print(f"\n\n---------- VALIDACIÓN DE QUE NINGÚN PARTICIPANTE SE REPITA EN LA ORDEN DE PRELACIÓN ----------")
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_orden_prelacion_1}")
        checarQueNingunParticipanteSeRepitaEnLaOrdenDePrelacion(prelacion1)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_orden_prelacion_2}")
        checarQueNingunParticipanteSeRepitaEnLaOrdenDePrelacion(prelacion2)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_orden_prelacion_3}")
        checarQueNingunParticipanteSeRepitaEnLaOrdenDePrelacion(prelacion3)

        # Checar que la suma de la longitud de la orden de prelación y la longitud de los ganadores sera igual al total
        print(f"\n\n---------- VALIDACIÓN DE QUE LA SUMA DEL NÚMERO DE GANADORES Y NO GANADORES SEA IGUAL AL NÚMERO TOTAL DE PARTICIPANTES ----------")
        print(f"\nVALIDANDO {archivo_terrenos_1} y {archivo_orden_prelacion_1}")
        checarQueLaSumaDeLosGanadoresYNoGanadoresSeaIgualAlTotal(df_participantes, prelacion1, terrenos1)
        print(f"\nVALIDANDO {archivo_terrenos_1} y {archivo_orden_prelacion_2}")
        checarQueLaSumaDeLosGanadoresYNoGanadoresSeaIgualAlTotal(df_participantes, prelacion2, terrenos1)
        print(f"\nVALIDANDO {archivo_terrenos_1} y {archivo_orden_prelacion_3}")
        checarQueLaSumaDeLosGanadoresYNoGanadoresSeaIgualAlTotal(df_participantes, prelacion3, terrenos1)
        print(f"\nVALIDANDO {archivo_terrenos_2} y {archivo_orden_prelacion_1}")
        checarQueLaSumaDeLosGanadoresYNoGanadoresSeaIgualAlTotal(df_participantes, prelacion1, terrenos2)
        print(f"\nVALIDANDO {archivo_terrenos_2} y {archivo_orden_prelacion_2}")
        checarQueLaSumaDeLosGanadoresYNoGanadoresSeaIgualAlTotal(df_participantes, prelacion2, terrenos2)
        print(f"\nVALIDANDO {archivo_terrenos_2} y {archivo_orden_prelacion_3}")
        checarQueLaSumaDeLosGanadoresYNoGanadoresSeaIgualAlTotal(df_participantes, prelacion3, terrenos2)
        print(f"\nVALIDANDO {archivo_terrenos_3} y {archivo_orden_prelacion_1}")
        checarQueLaSumaDeLosGanadoresYNoGanadoresSeaIgualAlTotal(df_participantes, prelacion1, terrenos3)
        print(f"\nVALIDANDO {archivo_terrenos_3} y {archivo_orden_prelacion_2}")
        checarQueLaSumaDeLosGanadoresYNoGanadoresSeaIgualAlTotal(df_participantes, prelacion2, terrenos3)
        print(f"\nVALIDANDO {archivo_terrenos_3} y {archivo_orden_prelacion_3}")
        checarQueLaSumaDeLosGanadoresYNoGanadoresSeaIgualAlTotal(df_participantes, prelacion3, terrenos3)

        # Checar que si juntamos a ganadores y no ganadores sean igual a la lista de participantes original
        print(f"\n\n---------- VALIDACIÓN DE QUE LA UNIÓN DE GANADORES Y NO GANADORES SEA IGUAL A LA LISTA ORIGINAL DE PARTICIPANTES ----------")
        print(f"\nVALIDANDO {archivo_terrenos_1} y {archivo_orden_prelacion_1}")
        checarQueUnionDeGanadoresYNoGanadoresEsIgualALaListaDeParticipantesOriginal(df_participantes, prelacion1, terrenos1)
        print(f"\nVALIDANDO {archivo_terrenos_1} y {archivo_orden_prelacion_2}")
        checarQueUnionDeGanadoresYNoGanadoresEsIgualALaListaDeParticipantesOriginal(df_participantes, prelacion2, terrenos1)
        print(f"\nVALIDANDO {archivo_terrenos_1} y {archivo_orden_prelacion_3}")
        checarQueUnionDeGanadoresYNoGanadoresEsIgualALaListaDeParticipantesOriginal(df_participantes, prelacion3, terrenos1)

        print(f"\nVALIDANDO {archivo_terrenos_2} y {archivo_orden_prelacion_1}")
        checarQueUnionDeGanadoresYNoGanadoresEsIgualALaListaDeParticipantesOriginal(df_participantes, prelacion1, terrenos2)
        print(f"\nVALIDANDO {archivo_terrenos_2} y {archivo_orden_prelacion_2}")
        checarQueUnionDeGanadoresYNoGanadoresEsIgualALaListaDeParticipantesOriginal(df_participantes, prelacion2, terrenos2)
        print(f"\nVALIDANDO {archivo_terrenos_2} y {archivo_orden_prelacion_3}")
        checarQueUnionDeGanadoresYNoGanadoresEsIgualALaListaDeParticipantesOriginal(df_participantes, prelacion3, terrenos2)

        print(f"\nVALIDANDO {archivo_terrenos_3} y {archivo_orden_prelacion_1}")
        checarQueUnionDeGanadoresYNoGanadoresEsIgualALaListaDeParticipantesOriginal(df_participantes, prelacion1, terrenos3)
        print(f"\nVALIDANDO {archivo_terrenos_3} y {archivo_orden_prelacion_2}")
        checarQueUnionDeGanadoresYNoGanadoresEsIgualALaListaDeParticipantesOriginal(df_participantes, prelacion2, terrenos3)
        print(f"\nVALIDANDO {archivo_terrenos_3} y {archivo_orden_prelacion_3}")
        checarQueUnionDeGanadoresYNoGanadoresEsIgualALaListaDeParticipantesOriginal(df_participantes, prelacion3, terrenos3)


print("\n\nLA VALIDACIÓN DE LOS DATAFRAMES SE HA REALIZADO CON ÉXITO")
        

        


        