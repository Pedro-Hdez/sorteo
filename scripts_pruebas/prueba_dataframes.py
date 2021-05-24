import os
import pandas as pd
from pandas._testing import assert_frame_equal

def checarUnicidadBoletos(df):
    # Obtenemos las listas de boletos de cada participante
    columna_boletos = [l[1:-1].split(', ') for l in df['boletos'].values]

    # Checamos lista por lista
    for i in range(len(columna_boletos)):
        # Sacamos la lista[0]
        lista_actual = columna_boletos.pop(0)
        # Comparamos cada boleto en la lista actual con los
        # boletos que se encuentran en las demás listas de boletos
        for boleto in lista_actual:
            for lista_restante in columna_boletos:
                # Si el boleto actual se encuentra en alguna otra lista de boletos,
                # entonces se dispara un error.
                if boleto in lista_restante:
                    raise AssertionError(f"El boleto {boleto} se repite")
        
        # Cuando hayamos validado la lista actual, entonces la volvemos a meter a 
        # la lista de listas de los boletos, pero hasta el final. De este modo
        # las siguentes validaciones también tomarán en cuenta a esta lista.
        columna_boletos.append(lista_actual)
    
    # Si se revisaron todos los boletos de todas las listas, entonces se despliega
    # un mensaje de éxito.
    print(f"La unicidad de los boletos se ha validado con éxito")

def checarNumeroDeBoletosAsignados(df):
    for registro in df.iterrows():
        lista_boletos = registro[1]['boletos'][1:-1].split(', ')
        # Checamos que la antigüedad coincida con la longitud de su lista de boletos
        if registro[1]['antiguedad'] != len(lista_boletos):
            # Si la antiguedad no coincide con el número de boletos asignados, se
            # dispara un error.
            raise AssertionError(f"La antigüedad del trabajador {registro[1]['num_empleado']} no coincide con el número de boletos que se le han asignado.")
    
    # Si se revisaron el número de boletos de todos los participantes, entonces se 
    # despliega un mensaje de éxito
    print(f"A todos los participantes se le han asignado el número correcto de boletos")

def checarUnicidadGanadores(df):
    if (len(pd.unique(df['boleto_ganador']))) != len(df.index):
        raise AssertionError('Se repite un boleto ganador')
    
    if (len(pd.unique(df['num_empleado']))) != len(df.index): 
        raise AssertionError('Un participante ganó más de una vez')
    
    print("Los boletos ganadores y los números de empleado ganadores son únicos.")


def checarCorrespondenciaBoletoGanador(df_boletos, df_ganadores):
    for i in range(len(df_ganadores.index)):
        terreno_actual = df_ganadores.iloc[i]
        boleto_ganador = terreno_actual['boleto_ganador']
        participante_ganador = terreno_actual['num_empleado']

        registro_participante_ganador = df_boletos[df_boletos['num_empleado'] == participante_ganador]
        boletos_participante_ganador = [l[1:-1].split(', ') for l in registro_participante_ganador['boletos'].values][0]

        if boleto_ganador not in boletos_participante_ganador:
            raise AssertionError(f'El boleto ganador {boleto_ganador} no pertenece al ganador {participante_ganador}')

        if participante_ganador != registro_participante_ganador['num_empleado'].values[0]:
            raise AssertionError(f'El ganador reportado es diferente al poseedor del boleto ganador')
    
    print("La correspondencia de los boletos ganadores con sus dueños se ha verificado con éxito.")


def checarIdentidadDataFrames(df1, df2):
    try:
        assert_frame_equal(df1, df2)
        print(f"Los dataframes son iguales")
    except:
        raise AssertionError(f'Los dataFrames son diferentes')

root = "./"
for f in os.listdir(root):
    folder = root+f
    if os.path.isdir(folder) and folder != "./datos":
        print(f"***** REVISANDO LAS CORRIDAS DE: {folder} *****")

        archivo_boletos_1 = folder+"/ASIGNACION_DE_BOLETOS_1.csv"
        archivo_boletos_2 = folder+"/ASIGNACION_DE_BOLETOS_2.csv"
        archivo_boletos_3 = folder+"/ASIGNACION_DE_BOLETOS_3.csv"

        archivo_terrenos_1 = folder+"/RESULTADOS_DEL_SORTEO_1.csv"
        archivo_terrenos_2 = folder+"/RESULTADOS_DEL_SORTEO_2.csv"
        archivo_terrenos_3 = folder+"/RESULTADOS_DEL_SORTEO_3.csv"

        # Se obtienen los csv de la asignación de boletos
        boletos1 = pd.read_csv(archivo_boletos_1, skiprows=3)
        boletos2 = pd.read_csv(archivo_boletos_2, skiprows=3)
        boletos3 = pd.read_csv(archivo_boletos_3, skiprows=3)

        # Se obtienen los csv de la asignación de terrenos
        terrenos1 = pd.read_csv(archivo_terrenos_1, skiprows=2)
        terrenos2 = pd.read_csv(archivo_terrenos_2, skiprows=2)
        terrenos3 = pd.read_csv(archivo_terrenos_3, skiprows=2)


        # Se checa que el número de boletos asignados a cada participante coincida
        # con sus años e antiguedad
        print(f"---------- VALIDACIÓN DEL NÚMERO DE BOLETOS ASIGNADOS A LOS PARTICIPANTES ----------")
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_boletos_1}")
        checarNumeroDeBoletosAsignados(boletos1)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_boletos_2}")
        checarNumeroDeBoletosAsignados(boletos2)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_boletos_3}")
        checarNumeroDeBoletosAsignados(boletos3)

        # Se checa la unicidad de los boletos en cada corrida
        print(f"\n\n---------- VALIDACIÓN DE LA UNICIDAD DE LOS BOLETOS ----------")
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_boletos_1}")
        checarUnicidadBoletos(boletos1)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_boletos_2}")
        checarUnicidadBoletos(boletos2)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_boletos_3}")
        checarUnicidadBoletos(boletos3)

        # Se checa la unicidad de los ganadores
        print(f"\n\n---------- VALIDACIÓN DE LA UNICIDAD DE LOS GANADORES ----------")
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_terrenos_1}")
        checarUnicidadGanadores(terrenos1)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_terrenos_2}")
        checarUnicidadGanadores(terrenos2)
        print(f"\nVALIDANDO EL ARCHIVO: {archivo_terrenos_3}")
        checarUnicidadGanadores(terrenos3)

        # Se checa la correspondencia de los boletos ganadores con sus dueños
        print(f"\n\n---------- VALIDACIÓN DE LA CORRESPONDENCIA DE LOS BOLETOS GANADORS CON SUS DUEÑOS ----------")
        print(f"\nVALIDANDO {archivo_boletos_1} y {archivo_terrenos_1}")
        checarCorrespondenciaBoletoGanador(boletos1, terrenos1)
        print(f"\nVALIDANDO {archivo_boletos_2} y {archivo_terrenos_2}")
        checarCorrespondenciaBoletoGanador(boletos2, terrenos2)
        print(f"\nVALIDANDO {archivo_boletos_3} y {archivo_terrenos_3}")
        checarCorrespondenciaBoletoGanador(boletos3, terrenos3)

        # Se checa que los tres dataframes de boletos sean idénticos
        print(f"\n\n---------- VALIDACIÓN DE LA IDENTIDAD DE LOS DATAFRAMES DE ASIGNACIÓN DE BOLETOS ----------")
        print(f"\nVALIDANDO {archivo_boletos_1} y {archivo_boletos_2}")
        checarIdentidadDataFrames(boletos1, boletos2)
        print(f"\nVALIDANDO {archivo_boletos_1} y {archivo_boletos_3}")
        checarIdentidadDataFrames(boletos1, boletos3)
        print(f"\nVALIDANDO {archivo_boletos_2} y {archivo_boletos_3}")
        checarIdentidadDataFrames(boletos2, boletos3)

        # Se checa que los tres dataframes de terrenos
        print(f"\n\n---------- VALIDACIÓN DE LA IDENTIDAD DE LOS DATAFRAMES DE ASIGNACIÓN DE TERRENOS ----------")
        print(f"\nVALIDANDO {archivo_terrenos_1} y {archivo_terrenos_2}")
        checarIdentidadDataFrames(terrenos1, terrenos2)
        print(f"\nVALIDANDO {archivo_terrenos_1} y {archivo_terrenos_3}")
        checarIdentidadDataFrames(terrenos1, terrenos3)
        print(f"\nVALIDANDO {archivo_terrenos_2} y {archivo_terrenos_3}")
        checarIdentidadDataFrames(terrenos2, terrenos3)
        print(f"\n\n\n")

print("LA VALIDACIÓN DE LOS DATAFRAMES SE HA REALIZADO CON ÉXITO")
        

        


        