
# ******************* DEPENDENCIAS Y CONFIGURACIÓN INICIAL ********************
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Label import Label
from dash.dependencies import Input, Output, State
#from dash_extensions import Download

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
                dbc.ModalHeader(html.H2("Establecer semilla para el sorteo de los boletos")),
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

# Modal para descargar los resultados del sorteo de boletos
descarga_resultados_sorteo_boletos_modal = html.Div(
    [        
        dbc.Modal(
            [
                dbc.ModalHeader(html.H2("Descarga de los resultados del sorteo de boletos"), style={'background-color':'#3D7EF2', 'color':'white'}),
                dbc.ModalBody(children=[
                    html.Div(children=[
                        html.H3("El sorteo de los boletos ha finalizado",style={'text-align':'center', 'padding':'1em'}),
                        
                        html.Div([
                            dbc.Button("Descargar el archivo de resultados en formato csv", 
                                    id="btn-descarga-resultados-sorteo-boletos", 
                                    color="success", className="mr-1"), 

                            dcc.Download(id="descarga-resultado-sorteo-boletos")
                        ],style={"display":'flex', "justify-content":"center", "align-items": "center"}),
                    ]),
                    
                ], style={'background-color':'#EBEBEB'}),
            ],
            id="descarga-resultado-sorteo-boletos-modal",
            is_open=False,
            size="xl", #sm, lg, xl
            backdrop=False, # to be or not to be closed by clicking on backdrop
            scrollable=True, # Scrollable if modal has a lot of text
            centered=True, 
            fade=True,
            keyboard=False
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
        'minWidth': 75, 'maxWidth': 75, 'width':75,
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
            'textAlign': 'left',
            'width':200
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
# -------------------------- OBJETOS DE LA FASE 2 ----------------------------


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

    # Objeto para almacenar la bandera que nos indica si el modal para la descarga de los
    # resultados del sorteo de boletos se abrirá o no
    dcc.Store(
        id='info-abrir-modal-descargar-resultados-sorteo-boletos', data=False
    ),

    # Objeto para almacenar la bandera que nos indicará si el botón de sortear participante
    # se deshabilita o no
    dcc.Store(
        id='info-deshabilitar-boton-sortear-participante', data=True
    ),

    # Objeto para almacenar la bandera que nos indicará si el botón de sortear participante
    # se habilitará
    dcc.Store(
        id='info-habilitar-boton-sortear-participante', data=False
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
            ], style={"position":"relative", "height":"800px", "overflow":"auto", "display":"block", "justify":"center"}, id='div-pila-datos-fase1'),
        ])
    ], style={"margin": "auto","width": "100%", 'padding':'1em', 'display':'none'}),

    # -------------------------------- Fase 2 ---------------------------------
    html.Div(id='div-fase2', children=[
        html.Div(children=[
            html.H1("FASE 2: SORTEO DE BOLETOS",style={'text-align':'center', 'padding':'1em'}),
        ]),

        # Modal para descargar el resultado del sorteo de los boletos
        descarga_resultados_sorteo_boletos_modal,

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
                    html.H3('PARTICIPANTE ACTUAL', style={'text-align':'center'}),
                    html.H3(children=[], style={'text-align':'center'}, 
                            id='participantes-restantes-label'),
                    
                    tabla_sorteo_fase2,

                    html.H3('LISTA DE BOLETOS DEL PARTICIPANTE ACTUAL', style={'text-align':'center'}),

                    tabla_boletos_fase2,

                    html.Br(),

                    dbc.Button("Los boletos no se han mezclado", id="siguiente-btn", color="primary", className="mr-1", style={'float':'right'}, disabled=True),
                    
                ], style={"margin": "auto","width": "85%", 'padding':'1em'})
            ],md=6)
            
        ]),
        
        html.Div([
            html.H3('PILA DE BOLETOS MEZCLADOS', style={'text-align':'center', 'padding':'1em'}),
            
        ], style={"margin": "auto","width": "85%", 'padding':'1em'}),
        
        html.Div([
        ], style={"position":"relative", "height":"800px", "overflow":"auto", "display":"block", "justify":"center", "margin": "0 auto", "width": "95%"}, id='div-pila-datos-fase2'),
 

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
    elif url == '/fase3':
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
     Output('div-pila-datos-fase1', 'children')],

    Input('link-fase1', 'n_clicks'),

    [State('info-tabla-participantes-fase1', 'data'), State('info-total-participantes', 'data'), 
     State('info-total-boletos', 'data'), State('info-num-columnas-pila-boletos', 'data'),
     State('div-pila-datos-fase1', 'children')],
)
def mostrarInfoFase1(link_fase1, tabla_participantes_fase1, total_participantes, total_boletos, 
                     n_cols, pila_datos_children):
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
            n_ceros = len(str(n_boletos))
            boletos = [str(i).zfill(n_ceros) for i in range(1, n_boletos+1)]
            # Se rellenan al final con datos en blanco
            boletos += [' ' for _ in range(num_completar)]

            # Se genera una tabla
            renglones = []
            i = 0
            for _ in range(num_renglones):
                renglon = html.Tr(children=[])
                for _ in range(n_cols):
                    renglon.children.append(html.Td(boletos[i], style={'min-width': "50px", 'max-width': "50px", 'width': "50px", 'text-align':'center'}))
                    i += 1
                renglones.append(renglon)
            
            table_body = html.Tbody(renglones)
            table = dbc.Table(table_body, bordered=True)


            return data_participantes, data_participantes, n_participantes, n_boletos, n_participantes, n_boletos, table
        else:
            print("YA EXISTE TODO, SE VA A ENVIAR DIRECTAMENTE")
            return dash.no_update
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
def mostrarModalSemilla(link_fase2, ok_btn_modal_semilla, modal_esta_abierto, info_semilla):
    contexto = dash.callback_context
    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        boton = contexto.triggered[0]['prop_id'].split('.')[0]

        if boton == 'link-fase2':
            if info_semilla == 'Sin semilla':
                print("Se necesita una nueva semilla")
                return not modal_esta_abierto
        elif boton == 'ok-boton-modal-semilla':
            print("Se cierra el modal")
            return not modal_esta_abierto
    else:
        return modal_esta_abierto

# ----> Callback para leer la semilla del modal y actualizarla en el objeto
#       dcc.Store y en su correspondiente etiqueta.
@app.callback(
    [Output('label-semilla', 'children'), Output('info-semilla', 'data')],
    [Input('link-fase2', 'n_clicks'), Input('ok-btn-modal-semilla', 'n_clicks')],
    [State('semilla-modal-form', 'children'), State('info-semilla', 'data')]
)
def actualizarSemilla(link_fase2, ok_btn_modal_semilla, modal_childrens, info_semilla):

    contexto = dash.callback_context
    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        boton = contexto.triggered[0]['prop_id'].split('.')[0]

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
            return dash.no_update
    else:
        return dash.no_update

# ----> Callback para realizar el sorteo de los boletos y notificar que se
#       realizó exitosamente. Además, se crea la pila de boletos mezclados. También se habilita
#       el botón para sortear participantes
@app.callback(
    [Output('afirmacion-sorteo-boletos-modal', 'is_open'), Output('sorteo-boletos', 'data'),
     Output('div-pila-datos-fase2', 'children'), Output('sorteo-boletos-btn', 'disabled'),
     Output('sorteo-boletos-btn', 'children'), Output('info-habilitar-boton-sortear-participante', 'data')],

    [Input('sorteo-boletos-btn', 'n_clicks'), Input('ok-afirmacion-sorteo-boletos-btn-modal', 'n_clicks')],

    [State('info-semilla', 'data'), State('sorteo-boletos', 'data'), 
     State('info-tabla-participantes-fase1', 'data'), State('info-num-columnas-pila-boletos', 'data'),
     State('div-pila-datos-fase2', 'children')]
)
def sortearBoletos(sorteo_boletos_btn, ok_btn_sorteo_boletos_modal, info_semilla, sorteo_boletos,
                   info_tabla_participantes, n_cols, pila_datos_children):
    contexto = dash.callback_context

    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        boton = contexto.triggered[0]['prop_id'].split('.')[0]

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
            
            # Se genera una tabla
            renglones = []
            i = 0
            for _ in range(num_renglones):
                renglon = html.Tr(children=[])
                for _ in range(n_cols):
                    renglon.children.append(html.Td(boletos[i], style={'min-width': "50px", 'max-width': "50px", 'width': "50px", 'text-align':'center'}))
                    i += 1
                renglones.append(renglon)
            
            table_body = html.Tbody(renglones)
            table = dbc.Table(table_body, bordered=True, id='tabla-pila-boletos-fase2')

            return True, df_sorteo.to_dict('records'), table, True, "Los boletos ya se han mezclado", True
        elif boton == 'ok-afirmacion-sorteo-boletos-btn-modal':
            print("OK")
            return False, sorteo_boletos, pila_datos_children, True, "Los boletos ya se han mezclado", True
    else:
        return dash.no_update

# ----> Callback para la visualización del sorteo de los boletos
# style_data_conditional=[{'if': {'row_index': i, 'column_id': 'COLOR'}, 'background-color': df['COLOR'][i], 'color': df['COLOR'][i]} for i in range(df.shape[0])]
@app.callback(
    [Output('tabla-participantes-fase2', 'data'), Output('idx-participante-sorteo-boletos', 'data'),
     Output('tabla-participante-actual', 'data'), Output('tabla-boletos-participante-actual', 'data'),
     Output('tabla-pila-boletos-fase2', 'children'), Output('participantes-restantes-label', 'children'), 
     Output('info-abrir-modal-descargar-resultados-sorteo-boletos', 'data'),
     Output('info-deshabilitar-boton-sortear-participante', 'data')],

    Input('siguiente-btn', 'n_clicks'),

    [State('idx-participante-sorteo-boletos', 'data'), State('sorteo-boletos', 'data'),
     State('tabla-participantes-fase2','data'), State('info-num-columnas-pila-boletos', 'data'),
     State('tabla-pila-boletos-fase2', 'children'), State('info-total-participantes', 'data')]
)
def mostrarSorteoBoletos(siguiente_btn, idx_participante, data_sorteo, datos_tabla_participantes, 
                         n_cols, pila_datos_children, total_participantes):
    # Convertimos a dataFrame la info del sorteo
    if siguiente_btn:
        df_sorteo = pd.DataFrame.from_dict(data_sorteo)

        # Tomamos el participante número idx_participante
        participante_actual = df_sorteo.to_dict('records')[idx_participante]

        # Se edita el formato de los boletos para la tabla de los participantes y 
        # la tabla de los boletos
        
        str_boletos = ""
        for boleto in participante_actual['boletos']:
            str_boletos += boleto + ", "
            
        

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
        registro_tabla_boletos = [{'boletos':str_boletos[:-2]}]

        # En la pila de boletos, se ponen en color azul los boletos del participante actual
        # y en rojo los que ya se han ocupado por otros participantes
        for renglon in pila_datos_children['props']['children']:
            for casilla in renglon['props']['children']:
                # Se les cambia el color a los boletos ya seleccionados (rojo)
                # Los identificamos porque en este momento tendrán su color de fondo como rojo
                try:
                    if casilla['props']['style']['background-color'] == '#0093E8' :
                        casilla['props']['style']['background-color'] = '#DE4B4B'
                except:
                    pass

                # Se les cambia el color a los boletos del participante actual (azul)
                if casilla['props']['children'] in participante_actual['boletos']:
                    casilla['props']['style']['background-color'] = '#0093E8'
                    casilla['props']['style']['color'] = '#FFFFFF'
        
        # Se crea una nueva etiqueta para indicar a los participantes restantes
        etiqueta_participantes_restantes = f"({total_participantes-idx_participante-1} restantes)"

        # Se decide si ya es necesario bloquear el botón de "siguiente participante"
        desactivar_boton = False
        abrir_modal_descarga_resultados = False
        deshabilitar_boton_sortear_participante = False
        if idx_participante == total_participantes - 1:
            desactivar_boton = True
            abrir_modal_descarga_resultados = True
            deshabilitar_boton_sortear_participante = True

        return datos_tabla_participantes, idx_participante+1, registro_participante_sorteado, registro_tabla_boletos, pila_datos_children, etiqueta_participantes_restantes, abrir_modal_descarga_resultados, deshabilitar_boton_sortear_participante
    else:
        return dash.no_update

# Callback para desplegar, en caso de ser necesario, el modal para descargar los resultados del
# sorteo de boletos
@app.callback(
    Output("descarga-resultado-sorteo-boletos-modal", 'is_open'),
    [Input('info-abrir-modal-descargar-resultados-sorteo-boletos', 'data'),
     Input("btn-descarga-resultados-sorteo-boletos", 'n_clicks')],
    State("descarga-resultado-sorteo-boletos-modal", 'is_open')
)
def mostrarModalDescargaResultadosSorteoBoletos(info_abrir_modal, btn_descarga, modal_esta_abierto):
    contexto = dash.callback_context
    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        elemento = contexto.triggered[0]['prop_id'].split('.')[0]
        if elemento == "info-abrir-modal-descargar-resultados-sorteo-boletos":
            if info_abrir_modal:
                return True
        elif elemento == 'btn-descarga-resultados-sorteo-boletos':
            return not modal_esta_abierto
    else:
        return modal_esta_abierto


# Callback para bloquear, el botón de sortear boletos a los participantes cuando este sorteo
# termine
@app.callback(
    [Output('siguiente-btn', 'disabled'), Output('siguiente-btn', 'children')],
    [Input('info-deshabilitar-boton-sortear-participante', 'data'),
     Input('info-habilitar-boton-sortear-participante', 'data')]
)
def deshabilitarBotonSortearSiguienteParticipante(deshabilitar, habilitar):
    contexto = dash.callback_context
    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        boton = contexto.triggered[0]['prop_id'].split('.')[0]

        if boton == 'info-deshabilitar-boton-sortear-participante':
            if deshabilitar:
                return True, "Sorteo finalizado"
            else:
                return False, "Sortear boletos al siguiente participante"

        elif boton == 'info-habilitar-boton-sortear-participante':
            if habilitar:
                return False, "Sortear boletos al siguiente participante"
            else:
                return True, "Los boletos no se han mezclado"
    else:
        return dash.no_update

    if deshabilitar:
        return True, "Sorteo finalizado"
    else:
        return False, "Sortear boletos al siguiente participante"

# Callback para descargar los resultados del sorteo de boletos
@app.callback(
    Output('descarga-resultado-sorteo-boletos', 'data'),
    Input('btn-descarga-resultados-sorteo-boletos', 'n_clicks'),
    State('sorteo-boletos', 'data'),
    prevent_initial_call=True
)
def descargarResultadoAsignacionBoletos(btn_descarga_resultados, diccionario_resultados_sorteo_boletos): 
    texto = pd.DataFrame.from_dict(diccionario_resultados_sorteo_boletos).to_csv(index=False)
    return dict(content=texto,filename="resultados_sorteo_boletos.csv")

if __name__ == '__main__':
    app.run_server(debug=True)