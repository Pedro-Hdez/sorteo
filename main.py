
# ******************* DEPENDENCIAS Y CONFIGURACIÓN INICIAL ********************
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Label import Label
from dash.dependencies import Input, Output, State

import dash_table
import pandas as pd
import math
import numpy as np


from sorteo import sorteoBoletos

external_stylesheets = [dbc.themes.COSMO]

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=external_stylesheets
               )


# -------------------------- OBJETOS DE LA FASE 1 ----------------------------
# Tabla para los participantes
tabla_participantes_fase1 = dash_table.DataTable(
    id='tabla-participantes-fase1',
    columns=[{"name": 'No. Empleado', "id": 'num_empleado'},
            {'name':'Nombre', 'id':'nombre'},
            {'name':'Apellido', 'id':'apellido'},
            {'name':'Antigüedad', 'id':'antiguedad'}],
    data=[],
    style_cell={
        'minWidth': 95, 'maxWidth': 95, 'width': 95,
        'text_align':'center'
    },
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
    },
    fixed_rows={'headers': True},
    style_table={'height': 800},
)

# -------------------------- OBJETOS DE LA FASE 2 ----------------------------
# Modal para pedir la semilla
semilla_modal_fase2 = html.Div(
    [        
        dbc.Modal(
            [
                dbc.ModalHeader("Establecer Semilla"),
                dbc.ModalBody(children=[
                    dbc.Form(id='semilla-modal-form',
                        children=[
                            dbc.FormGroup(
                                [
                                    dbc.Label("Día: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text")
                                ],
                                className="mr-3"
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("Mes: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text")
                                ],
                                className="mr-3"
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("Año: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text")
                                ],
                                className="mr-3"
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("Hora: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text")
                                ],
                                className="mr-3"
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("Minuto: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text")
                                ],
                                className="mr-3"
                            )
                        ],
                        inline=True
                    )]
                ),
                dbc.ModalFooter(
                    html.Div(
                        [
                            dbc.Button("Ok", id="ok-btn-modal-semilla", color="primary", 
                                    style={'margin':"1em"},)
                        ]
                    )
                )
            ],
            id="semilla-modal",
            is_open=False,
            size="xl", #sm, lg, xl
            backdrop=False, # to be or not to be closed by clicking on backdrop
            scrollable=True, # Scrollable if modal has a lot of text
            centered=False, 
            fade=True,
            keyboard=False
        )
    ]
)

# Modal para avisar que el sorteo se ha realizado
afirmacion_sorteo_boletos_modal_fase2 = html.Div(
    [        
        dbc.Modal(
            [
                dbc.ModalHeader(""),
                dbc.ModalBody(children=[
                    html.Div(children=[
                        html.H3("LOS BOLETOS SE HAN TERMINADO DE MEZCLAR",style={'text-align':'center', 'padding':'1em'}),
                    ]),
                    
                ]),
                dbc.ModalFooter(
                    html.Div(
                        [
                            dbc.Button("Ok", id="ok-afirmacion-sorteo-boletos-btn-modal", color="primary", 
                                    style={'margin':"1em"},)
                        ]
                    )
                )
            ],
            id="afirmacion-sorteo-boletos-modal",
            is_open=False,
            size="sm", #sm, lg, xl
            backdrop=True, # to be or not to be closed by clicking on backdrop
            scrollable=True, # Scrollable if modal has a lot of text
            centered=True, 
            fade=True,
            keyboard=True
        )
    ]
)

# Etiqueta para mostrar la semilla
semilla_label = dbc.Label(html.H3("Semilla: Sin semilla", id='label-semilla'), 
                          style={'text-align':'center', 'padding':'1em'})

# Tabla de los participantes que ya tiene boletos
tabla_participantes_fase2 = dash_table.DataTable(
    id='tabla-participantes-fase2',
    columns=[{"name": 'No. Empleado', "id": 'num_empleado'},
            {'name':'Nombre', 'id':'nombre'},
            {'name':'Apellido', 'id':'apellido'},
            {'name':'Antigüedad', 'id':'antiguedad'},
            {'name':'Boletos', 'id':'boletos'}],
    data=[],

    style_cell={
        'text_align':'center',
        'minWidth': 75, 'maxWidth': 200,
        'whiteSpace': 'pre-line',
        'height': 'auto',
    },

    style_data={
        'whiteSpace': 'pre-line',
        'height': 'auto',
    },

    style_cell_conditional=[
        {
            'if': {'column_id': 'boletos'},
            'textAlign': 'left'
        }
    ],
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'text-align':'center'
    },
    fixed_rows={'headers': True},
    style_table={'height': 800},
)

# Tabla para el participante actual al que le están dando sus boletos
tabla_sorteo_fase2 = dash_table.DataTable(
    id='tabla-participante-actual',
    columns=[{"name": 'No. Empleado', "id": 'num_empleado'},
             {'name':'Nombre', 'id':'nombre'},
             {'name':'Apellido', 'id':'apellido'},
             {'name':'Antigüedad', 'id':'antiguedad'}],
    data=[],
    style_cell={
        'text_align':'center',
        'minWidth': 75, 'maxWidth': 200, 'width':75,
        'whiteSpace': 'pre-line',
        'height': 'auto',
    },
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
    },
    fixed_rows={'headers': True},
    style_table={'height': 100},
)

# Tabla para mostrar los boletos del participante actual
tabla_boletos_fase2 = dash_table.DataTable(
    id='tabla-boletos-participante-actual',
    columns=[{'name':'boletos', 'id':'boletos'}],
    merge_duplicate_headers=True,
    data=[],
    style_cell={
        'text_align':'left',
        'minWidth': 90, 'maxWidth': 120, 'width': 120,
        'whiteSpace': 'pre-line',
        'height': 'auto',
    },
    style_data={
        'whiteSpace': 'pre-line',
        'height': 'auto',
    },
    style_header={
        'backgroundColor': 'white',
        'color': 'white'
    },
    fixed_rows={'headers': True},
    style_table={'height': 200},
)

# Tabla para la pila de boletos ordenados (Fase 1)
tabla_pila_boletos_fase1 = dash_table.DataTable(
    id='tabla-pila-boletos-fase1',
    columns=[],
    merge_duplicate_headers=True,
    data=None,
    style_cell={
        'minWidth': 40, 'maxWidth': 40, 'width': 40,
        'text_align':'center'
    },
    style_header={
        'backgroundColor': 'white',
        'color': 'white'
    },
    fixed_rows={'headers': True},
    #style_table={'height': 1500, 'overflowY':'auto'},
    css=[{"selector": "table", "rule": "width: 100%;"},{"selector": ".dash-spreadsheet.dash-freeze-top, .dash-spreadsheet .dash-virtualized", "rule": "max-height: 800px;"}]

)

# Tabla para la pila de boletos (Fase 2)
tabla_pila_boletos_fase2 = dash_table.DataTable(
    id='tabla-pila-boletos-fase2',
    columns=[],
    merge_duplicate_headers=True,
    data=None,
    style_cell={
        'minWidth': 40, 'maxWidth': 40, 'width': 40,
        'text_align':'center'
    },
    style_header={
        'backgroundColor': 'white',
        'color': 'white'
    },
    style_data_conditional=[],
    fixed_rows={'headers': True},
    #style_table={'height': 1500, 'overflowY':'auto'},
    css=[{"selector": "table", "rule": "width: 100%;"},{"selector": ".dash-spreadsheet.dash-freeze-top, .dash-spreadsheet .dash-virtualized", "rule": "max-height: 800px;"}]

)

# ***************************** PÁGINA PRINCIPAL ******************************

app.layout = html.Div([
    # ---------- OBJETOS DE ALMACENAMIENTO DE DATOS ----------

    # Objeto para almacenar la tabla de participantes de la fase 1
    dcc.Store(
        id='info-tabla-participantes-fase1', data=None
    ),

    # Objeto para almacenar el total de participantes
    dcc.Store(
        id='info-total-participantes', data=None
    ),

    # Objeto para almacenar el total de boletos
    dcc.Store(
        id='info-total-boletos', data=None
    ),

    # Objeto para almacenar la semilla de la generación aleatoria de boletos
    dcc.Store(
        id='info-semilla', data='Sin semilla'
    ),

    # Objeto para almacenar la asignación de boletos a los participantes
    dcc.Store(
        id='sorteo-boletos', data=None
    ),

    # Objeto para almacenar el siguiente participante a sortear
    dcc.Store(
        id='idx-participante-sorteo-boletos', data=0
    ),

    # Objeto para almacenar la pila de boletos
    dcc.Store(
        id='info-pila-boletos-mezclados', data=None
    ),

    # Objeto para almacenar las columnas de la tabla de la pila de boletos
    dcc.Store(
        id='info-columnas-tabla-pila-boletos', data=None
    ),

    # Objeto para almacenar las columnas de la tabla de la pila de boletos
    dcc.Store(
        id='info-num-columnas-pila-boletos', data=32
    ),

    # Objeto para almacenar el estilo
    dcc.Store(
        id='info-estilo-casillas', data=[]
    ),

    # Modal para pedir una semilla
    semilla_modal_fase2,
    

    # Objeto para la identificación de las rutas
    dcc.Location(id='url'),

    # Navbar de las fases
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Fase 1: Conteo de Boletos", href="/fase1", id='link-fase1')),
            dbc.NavItem(dbc.NavLink("Fase 2: Sorteo de Boletos", href="/fase2", id='link-fase2')),
            dbc.NavItem(dbc.NavLink("Fase 3: Sorteo de Terrenos", href="#", id='link-fase3')),
        ],
        brand="Fases del Sorteo",
        brand_href="/",
        color="primary",
        dark=True,
    ),

    #  ------------------ CONTENIDO PRINCIPAL DE LA PÁGINA --------------------

    # "Landing page"
    html.Div(id='div-principal', children=[
        html.H3("¡BIENVENIDOS Y MUCHA SUERTE!",style={'text-align':'center', 'padding':'1em'}),
    ]),


    # -------------------------------- Fase 1 ---------------------------------
    html.Div(id='div-fase1', children=[
        html.Div(children=[
            html.H1("FASE 1: CONTEO DE BOLETOS",style={'text-align':'center', 'padding':'1em'}),
        ]),

        html.H3('TABLA DE PARTICIPANTES', style={'text-align':'center', 'padding':'1em'}),
        
        tabla_participantes_fase1,
        
        html.Br(),
        html.Br(),
        
        html.Br(),
        dbc.Label(html.H3("Total de boletos: ")),
        dbc.Label(html.H3("", id='total-boletos-label'), style={'padding':'1em'}),

        html.Br(),
        dbc.Label(html.H3("Número de participantes: ")),
        dbc.Label(html.H3("", id='total-participantes-label'), style={'padding':'1em'}),

        dbc.Row([
            html.Div([
                html.H3('PILA DE BOLETOS', style={'text-align':'center', 'padding':'1em'}),
                
            ], style={"margin": "auto","width": "85%", 'padding':'1em'}),
            
            html.Div([
                tabla_pila_boletos_fase1,
            ], style={'text-align':'center', 'width':'100%'}),
        ])
    ], style={"margin": "auto","width": "100%", 'padding':'1em', 'display':'none'}),

    # -------------------------------- Fase 2 ---------------------------------
    html.Div(id='div-fase2', children=[
        html.Div(children=[
            html.H1("FASE 2: SORTEO DE BOLETOS",style={'text-align':'center', 'padding':'1em'}),
        ]),

        # Modal de confirmación cuando el sorteo se realice
        afirmacion_sorteo_boletos_modal_fase2, 
        
        dbc.Row([
            dcc.Loading(
                    id="loading-2",
                    children=[html.Div([html.Div(id="loading-output-2")])],
                    type="circle",
                ),
            dbc.Col([
                html.Div([
                    semilla_label, 
                    html.Br(),
                    dbc.Button("Mezclar boletos", id="sorteo-boletos-btn", 
                               color="success", className="mr-1", style={'margin-left':'15px'})
                ],style={'text-align':'left', 'margin':'auto'}),
                

                html.Div([
                    html.H3('PARTICIPANTES CON BOLETOS', style={'text-align':'center', 'padding':'1em'}),
                    
                    tabla_participantes_fase2,
                    
                ], style={"margin": "auto","width": "85%", 'padding':'1em'})
            ],md=6),

            dbc.Col([
                html.Div([
                    html.H3('PARTICIPANTE ACTUAL', style={'text-align':'center', 'padding':'1em'}),
                    
                    tabla_sorteo_fase2,

                    html.H3('LISTA DE BOLETOS DEL PARTICIPANTE ACTUAL', style={'text-align':'center', 'padding':'1em'}),

                    tabla_boletos_fase2,

                    html.Br(),

                    dbc.Button("Sortear boletos al siguiente participante", id="siguiente-btn", color="primary", className="mr-1", style={'float':'right'}),
                    
                ], style={"margin": "auto","width": "85%", 'padding':'1em'})
            ],md=6)
            
        ]),

        dbc.Row([
            html.Div([
                html.H3('PILA DE BOLETOS MEZCLADOS', style={'text-align':'center', 'padding':'1em'}),
                tabla_pila_boletos_fase2,
                
            ], style={"margin": "auto","width": "85%", 'padding':'1em'})  
        ])
    ], style={'display':"none"})
])




# ********************************* CALLBACKS *********************************

# ----> Callback para actualizar el contenido de la página i.e. el cambio de
#       fase ocultando o mostrando elementos 
@app.callback(
    [Output('div-principal', 'style'), Output('div-fase1', 'style'), Output('div-fase2', 'style'), 
     Output('link-fase1', 'style'), Output('link-fase2', 'style'), Output('link-fase3', 'style')],
    Input('url', 'pathname')
)
def cambiarFase(url):
    if url == '/':
        return {}, {'display':'none'}, {'display':'none'}, {}, {}, {}
    if url == '/fase1':
        return {'display':'none'}, {"margin": "auto","width": "85%", 'padding':'1em'}, {'display':'none'}, {"font-weight": "1000", 'color':'white'}, {}, {}
    elif url == '/fase2':
        return {'display':'none'}, {'display':'none'}, {}, {}, {"font-weight": "1000", 'color':'white'}, {}
    elif url == '/page3':
        return '/'

    # Objeto para almacenar las columnas de la tabla de la pila de boletos
    dcc.Store(
        id='info-columnas-tabla-pila-boletos', data=None
    ),
# *************************** CALLBACKS DE LA FASE 1 **************************
# ----> Callback para crear la tabla de los participante, calcular el total de
#       participantes y boletos, y guardarlos. Además, se crea la pila de boletos
#       ordenada.
@app.callback(
    [Output('tabla-participantes-fase1', 'data'), Output('info-tabla-participantes-fase1', 'data'),
     Output('total-participantes-label', 'children'), Output('total-boletos-label', 'children'),
     Output('info-total-participantes', 'data'), Output('info-total-boletos', 'data'),
     Output('tabla-pila-boletos-fase1', 'columns'), Output('tabla-pila-boletos-fase1', 'data'),
     Output('info-columnas-tabla-pila-boletos', 'data')],

    Input('link-fase1', 'n_clicks'),

    [State('info-tabla-participantes-fase1', 'data'), State('info-total-participantes', 'data'), 
     State('info-total-boletos', 'data'), State('tabla-pila-boletos-fase1', 'columns'), 
     State('tabla-pila-boletos-fase1', 'data'), State('info-columnas-tabla-pila-boletos', 'data'),
     State('info-num-columnas-pila-boletos', 'data')],
)
def mostrarInfoFase1(link_fase1, tabla_participantes_fase1, total_participantes,
                     total_boletos, cols_tabla_pila_boletos_fase1, data_tabla_pila_boletos_fase1,
                     info_columnas_tabla, n_cols):
    if link_fase1:
        # Si no tenemos una tabla, entonces la creamos y calculamos los totales de boletos y
        # participantes
        if not tabla_participantes_fase1 and not total_participantes and not total_boletos:
            print("NO HAY NADA, SE VA A CALCULAR TODO")
            # ----- Creación del DataFrame de los participantes -----
            df_participantes = pd.read_csv('../datos/participantes.csv')
            df_participantes = df_participantes.sort_values(by=['antiguedad', 'apellido'], 
                                                            ascending=[False, True])

            # Se calcula el total de participantes y el total de los boletos
            n_participantes = len(df_participantes.index)
            n_boletos = int(df_participantes['antiguedad'].sum())

            # Se formatea la información del DataFrame
            data_participantes = df_participantes.to_dict('records')

            # ----- Generación de los boletos  -----
            # Se calcula el total de renglones para la pila de boletos, considerando que 
            # utilizaremos 100 columnas. Además, se calcularán los datos que harán falta para
            # rellenar.
            print("NO HAY COLUMNAS, LAS VAMOS A CALCULAR")
            print(f"Tenemos {n_boletos}")
            print(f"Si dividimos entre {n_cols}, entonces: {n_boletos/n_cols}")
            num_renglones = math.ceil(n_boletos/n_cols)
            print(f"Por lo tanto, si tenemos {n_cols} columnas, necesitamos:{num_renglones} renglones!")
            num_completar = (math.ceil(n_boletos/n_cols) * n_cols) - n_boletos
            print(f"Y necesitamos completar con: {num_completar} espacios en blanco")

            # Se genera la secuencia de boletos
            n_ceros = len(str(n_boletos+1))
            boletos = [str(i).zfill(n_ceros) for i in range(1, n_boletos+1)]
            # Se rellenan al final con datos en blanco
            boletos += [' ' for _ in range(num_completar)]
            # Se les da la dimensión deseada (num_renglonesx100)
            boletos = np.array(boletos).reshape(num_renglones, n_cols)
            # Se crea un dataFrame
            df_boletos = pd.DataFrame(index=range(num_renglones), columns=range(n_cols), data=boletos)
            print(df_boletos)

            # ----- Generación de las columnas y los datos de la pila de boletos -----
            columnas_pila_boletos = [{'name':f'{i}', 'id':f'{i}'} for i in range(0, n_cols)]
            datos_pila_boletos = df_boletos.to_dict('records')

            return data_participantes, data_participantes, n_participantes, n_boletos, n_participantes, n_boletos, columnas_pila_boletos, datos_pila_boletos, columnas_pila_boletos
        else:
            print("YA EXISTE TODO, SE VA A ENVIAR DIRECTAMENTE")
            print(total_participantes)
            print(total_boletos)
            return tabla_participantes_fase1, tabla_participantes_fase1, total_participantes, total_boletos, total_participantes, total_boletos, cols_tabla_pila_boletos_fase1, data_tabla_pila_boletos_fase1, info_columnas_tabla
    else:
        return dash.no_update



# *************************** CALLBACKS DE LA FASE 2 **************************
# ----> Callback para revisar si es necesario introducir una nueva semilla para
#       el sorteo de los boletos
@app.callback(
    Output('semilla-modal', 'is_open'),
    [Input('link-fase2', 'n_clicks'), Input('ok-btn-modal-semilla', 'n_clicks')],
    [State('semilla-modal', 'is_open'), State('info-semilla', 'data')]
)
def mostrarModalSemilla(link_fase2, ok_btn_modal_semilla, is_modal_open, info_semilla):
    ctx = dash.callback_context
    if ctx.triggered:
        # Getting the id of the object which triggered the callback
        boton = ctx.triggered[0]['prop_id'].split('.')[0]

        if boton == 'link-fase2':
            if info_semilla == 'Sin semilla':
                print("Se necesita una nueva semilla")
                return not is_modal_open
        elif boton == 'ok-boton-modal-semilla':
            print("Se cierra el modal")
            return not is_modal_open
    else:
        return is_modal_open

# ----> Callback para leer la semilla del modal y actualizarla en el objeto
#       dcc.Store y en su correspondiente etiqueta.
@app.callback(
    [Output('label-semilla', 'children'), Output('info-semilla', 'data')],
    [Input('link-fase2', 'n_clicks'), Input('ok-btn-modal-semilla', 'n_clicks')],
    [State('semilla-modal-form', 'children'), State('info-semilla', 'data')]
)
def actualizarSemilla(link_fase2, ok_btn_modal_semilla, modal_childrens, info_semilla):

    ctx = dash.callback_context
    if ctx.triggered:
        # Getting the id of the object which triggered the callback
        boton = ctx.triggered[0]['prop_id'].split('.')[0]

        if boton == 'ok-btn-modal-semilla':
            print("Leyendo la semilla...")
            # Se obtiene la semilla introducida
            dia = modal_childrens[0]['props']['children'][1]['props']['value']
            mes = modal_childrens[1]['props']['children'][1]['props']['value']
            anio = modal_childrens[2]['props']['children'][1]['props']['value']
            hora = modal_childrens[3]['props']['children'][1]['props']['value']
            minuto = modal_childrens[4]['props']['children'][1]['props']['value']

            semilla = f"Semilla: {dia.zfill(2)}/{mes.zfill(2)}/{anio} {hora.zfill(2)}:{minuto.zfill(2)}"

            return semilla, semilla
        elif boton == 'link-fase2':
            print("se mantiene la semilla")
            return info_semilla, info_semilla
    else:
        return dash.no_update

# ----> Callback para realizar el sorteo de los boletos y notificar que se
#       realizó exitosamente. Además, se crea la pila de boletos mezclados
@app.callback(
    [Output('afirmacion-sorteo-boletos-modal', 'is_open'), Output('sorteo-boletos', 'data'),
     Output('info-pila-boletos-mezclados', 'data'), Output('tabla-pila-boletos-fase2', 'columns'), 
     Output('tabla-pila-boletos-fase2', 'data')],

    [Input('sorteo-boletos-btn', 'n_clicks'), Input('ok-afirmacion-sorteo-boletos-btn-modal', 'n_clicks')],

    [State('info-semilla', 'data'), State('sorteo-boletos', 'data'), 
     State('info-tabla-participantes-fase1', 'data'), State('info-num-columnas-pila-boletos', 'data'),
     State('tabla-pila-boletos-fase2', 'columns'), State('tabla-pila-boletos-fase2', 'data')]
)
def sortearBoletos(sorteo_boletos_btn, ok_btn_sorteo_boletos_modal, info_semilla, sorteo_boletos,
                   info_tabla_participantes, n_cols, columnas_pila_boletos_mezclados,
                   datos_pila_boletos_mezclados):
    ctx = dash.callback_context

    if ctx.triggered:
        # Getting the id of the object which triggered the callback
        boton = ctx.triggered[0]['prop_id'].split('.')[0]

        if boton == 'sorteo-boletos-btn':
            # Se obtiene el DataFrame de la fase anterior
            df_participantes = pd.DataFrame.from_dict(info_tabla_participantes)
            # Se realiza el sorteo de los boletos con la semilla dada.
            df_sorteo, pila_boletos_mezclados = sorteoBoletos(df_participantes, info_semilla)
            print(df_sorteo)

            n_boletos = len(pila_boletos_mezclados) # Número de boletos
            num_renglones = math.ceil(n_boletos/n_cols) # Número de renglones 
            # Número de casillas por completar
            num_completar = (math.ceil(n_boletos/n_cols) * n_cols) - n_boletos 

            # Se rellenan, al final, los boletos mezclados con datos en blanco
            boletos = pila_boletos_mezclados + [' ' for _ in range(num_completar)]
            # Se les da la dimensión deseada (num_renglonesx100)
            boletos = np.array(boletos).reshape(num_renglones, n_cols)
            # Se crea un dataFrame
            df_boletos = pd.DataFrame(index=range(num_renglones), columns=range(n_cols), data=boletos)

            # ----- Generación de las columnas y los datos de la pila de boletos -----
            columnas_pila_boletos = [{'name':f'{i}', 'id':f'{i}'} for i in range(0, n_cols)]
            datos_pila_boletos = df_boletos.to_dict('records')

            return True, df_sorteo.to_dict('records'), datos_pila_boletos, columnas_pila_boletos, datos_pila_boletos
        elif boton == 'ok-afirmacion-sorteo-boletos-btn-modal':
            print("OK")
            return False, sorteo_boletos, datos_pila_boletos_mezclados, columnas_pila_boletos_mezclados, datos_pila_boletos_mezclados 
    else:
        return dash.no_update

# ----> Callback para la visualización del sorteo de los boletos
# style_data_conditional=[{'if': {'row_index': i, 'column_id': 'COLOR'}, 'background-color': df['COLOR'][i], 'color': df['COLOR'][i]} for i in range(df.shape[0])]
@app.callback(
    [Output('tabla-participantes-fase2', 'data'), Output('idx-participante-sorteo-boletos', 'data'),
     Output('tabla-participante-actual', 'data'), Output('tabla-boletos-participante-actual', 'data'),
     Output('tabla-pila-boletos-fase2', 'style_data_conditional')],
    Input('siguiente-btn', 'n_clicks'),
    [State('idx-participante-sorteo-boletos', 'data'), State('sorteo-boletos', 'data'),
     State('tabla-participantes-fase2','data'), State('info-num-columnas-pila-boletos', 'data'),
     State('tabla-pila-boletos-fase2', 'style_data_conditional')]
)
def mostrarSorteoBoletos(siguiente_btn, idx_participante, data_sorteo, datos_tabla_participantes, n_cols, estilo_casillas_ocupadas):
    # Convertimos a dataFrame la info del sorteo
    if siguiente_btn:
        df_sorteo = pd.DataFrame.from_dict(data_sorteo)

        # Tomamos el participante número idx_participante
        participante_actual = df_sorteo.to_dict('records')[idx_participante]

        # Se edita el formato de los boletos para la tabla de los participantes y 
        # la tabla de los boletos
        i = 0
        j = 0
        str_boletos = ""
        str_boletos2 = ""
        for boleto in participante_actual['boletos']:
            if i == 5:
                str_boletos += "\n"
                i = 0

            if j == 14:
                str_boletos2 += "\n"
                j = 0

            str_boletos += boleto + ", "
            str_boletos2 += boleto + ", "
            i += 1
            j += 1

        # Se crea su registro en la tabla de Participantes con Boleto y se agrega
        registro_participantes_con_boleto = {'num_empleado':participante_actual['num_empleado'],
                                             'nombre':participante_actual['nombre'],
                                             'apellido':participante_actual['apellido'],
                                             'antiguedad':participante_actual['antiguedad'],
                                             'boletos':str_boletos[:-2]}
        datos_tabla_participantes.append(registro_participantes_con_boleto)
        
        # Se crea su registro en la tabla de Participante Sorteado
        registro_participante_sorteado = [{'num_empleado':participante_actual['num_empleado'],
                                           'nombre':participante_actual['nombre'],
                                           'apellido':participante_actual['apellido'],
                                           'antiguedad':participante_actual['antiguedad']}]
        
        # Se crea el registro con la lista de los boletos para añadirla a la lista de sus boletos
        registro_tabla_boletos = [{'boletos':str_boletos2[:-2]}]

        # Se ponen de color rojo todas las casillas que se metieron en la iteración anterior
        if estilo_casillas_ocupadas:
            # Se busca el número de boletos de la persona anterior
            n_boletos_anteriores = df_sorteo.to_dict('records')[idx_participante-1]['antiguedad'] * n_cols

            # A esos útlimos 'n_boletos_anteriores' boletos se les deberá cambiar el color a rojo
            for d in estilo_casillas_ocupadas[len(estilo_casillas_ocupadas)-n_boletos_anteriores:]:
                d['backgroundColor'] = '#BF1D1D'
        
        # Se agregan en color azul las casillas del participante actual
        estilo_casillas_ocupadas += [{'if': {'filter_query': f'{{{i}}} = {j}','column_id': f'{i}'},'backgroundColor': '#1173CF','color': 'white'} for i in range(0, n_cols) for j in participante_actual['boletos']]

        return datos_tabla_participantes, idx_participante+1, registro_participante_sorteado, registro_tabla_boletos, estilo_casillas_ocupadas
    else:
        return dash.no_update


#     else:
#         return dash.no_update


if __name__ == '__main__':
    app.run_server(debug=True)