
# ******************* DEPENDENCIAS Y CONFIGURACIÓN INICIAL ********************
from os import link
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Div import Div
from dash_html_components.Label import Label
from dash.dependencies import Input, Output, State

import dash_table
import pandas as pd
import math
import time


from sorteo import sorteoNumeros, sorteoLotes, sorteoListaPrelacion

external_stylesheets = [dbc.themes.COSMO]

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=external_stylesheets,
                assets_folder='assets',
                title="Sorteo Trece Lotes - Universidad de Sonora"
               )


# -------------------------- OBJETOS DE LA ETAPA 1 ----------------------------
# Tabla para los participantes
tabla_participantes_etapa1 = dash_table.DataTable(
    id='tabla-participantes-etapa1',
    columns=[{"name": 'No. Empleado', "id": 'num_empleado'},
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

# -------------------------- OBJETOS DE LA ETAPA 2 ----------------------------
# Modal para pedir la semilla
semilla_modal_etapa2 = html.Div(
    [        
        dbc.Modal(
            [
                dbc.ModalHeader(html.H2("Establecer semilla para la asignación de los números"), style={'background-color':'#3D7EF2', 'color':'white'}),

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
                        ],inline=True
                    ),
                    html.Div(
                    [
                        dbc.Button("Confirmar", id="ok-btn-modal-semilla", color="success", 
                                style={'margin':"1em", 'float':'right'},)
                    ]
                    )
                ], style={'background-color':'#EBEBEB'},),
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
afirmacion_sorteo_boletos_modal_etapa2 = html.Div(
    [        
        dbc.Modal(
            [
                dbc.ModalHeader(html.H2('Mezcla de los números'), style={'background-color':'#3D7EF2', 'color':'white'}),
                dbc.ModalBody(children=[
                    html.Div(children=[
                        html.H3("LOS NÚMEROS SE HAN TERMINADO DE MEZCLAR",style={'text-align':'center', 'padding':'1em'}),
                    ]),

                    html.Div(
                    [
                        dbc.Button("Continuar", id="ok-afirmacion-sorteo-boletos-btn-modal", color="success")
                    ], style={"display":'flex', "justify-content":"center", "align-items": "center"},
                )
                    
                ], style={'background-color':'#EBEBEB'}),


                
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
                dbc.ModalHeader(html.H2("Descarga de los resultados de la asignación de números"), style={'background-color':'#3D7EF2', 'color':'white'}),
                dbc.ModalBody(children=[
                    html.Div(children=[
                        html.H3("La asignación de los números ha finalizado",style={'text-align':'center', 'padding':'1em'}),
                        
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
tabla_participantes_etapa2 = dash_table.DataTable(
    id='tabla-participantes-etapa2',
    columns=[{"name": 'No. Empleado', "id": 'num_empleado'},
            {'name':'Antigüedad', 'id':'antiguedad'},
            {'name':'Números', 'id':'numeros'}],
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
            'if': {'column_id': 'numeros'},
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
tabla_sorteo_etapa2 = dash_table.DataTable(
    id='tabla-participante-actual',
    columns=[{"name": 'No. Empleado', "id": 'num_empleado'},
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
tabla_boletos_etapa2 = dash_table.DataTable(
    id='tabla-boletos-participante-actual',
    columns=[{'name':'numeros', 'id':'numeros'}],
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

# Leyenda para la pila de boletos mezclados de la etapa 2
leyenda_pila_datos_etapa2 = html.Ul([
    html.Li([
        html.Span([
        ], style={'border':'3px solid #000000', 'float':'left', 'width':'20px', 'height':'20px', 
                  'margin':'2px', 'background-color':'#FFFFFF'}),
        
        html.H5('Disponible', style={'float':'right'}),

    ], style={'float':'left', 'margin-right':'10px'}),

    html.Li([
        html.Span([
        ], style={'border':'3px solid #000000', 'float':'left', 'width':'20px', 'height':'20px', 
                  'margin':'2px', 'background-color':'#DE4B4B'}),

        html.H5('No disponible', style={'float':'right'}),

    ], style={'float':'left', 'margin-right':'10px'}),

    html.Li([
        html.Span([
        ], style={'border':'3px solid #000000', 'float':'left', 'width':'20px', 'height':'20px', 
                  'margin':'2px', 'background-color':'#0093E8'}),

        html.H5('Asignado al participante actual', style={'float':'right'}),

    ], style={'float':'left', 'margin-right':'10px'})
], style={'list-style':'none'})

# -------------------------- OBJETOS DE LA ETAPA 3 ----------------------------

# Modal para pedir la semilla
semilla_modal_etapa3 = html.Div(
    [        
        dbc.Modal(
            [
                dbc.ModalHeader(html.H2("Establecer semilla para el sorteo de los lotes"), style={'background-color':'#3D7EF2', 'color':'white'}),

                dbc.ModalBody(children=[
                    dbc.Form(id='semilla-modal-form-etapa3',
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
                        ],inline=True
                    ),
                    html.Div(
                    [
                        dbc.Button("Confirmar", id="ok-btn-modal-semilla-etapa3", color="success", 
                                style={'margin':"1em", 'float':'right'},)
                    ]
                    )
                ], style={'background-color':'#EBEBEB'},),
            ],
            id="semilla-modal-etapa3",
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

# Modal para descargar los resultados del sorteo de terrenos
descarga_resultados_sorteo_terrenos_modal = html.Div(
    [        
        dbc.Modal(
            [
                dbc.ModalHeader(html.H2("Descarga de los resultados del sorteo de lotes"), style={'background-color':'#3D7EF2', 'color':'white'}),
                dbc.ModalBody(children=[
                    html.Div(children=[
                        html.H3("El sorteo de los lotes ha finalizado",style={'text-align':'center', 'padding':'1em'}),
                        
                        html.Div([
                            dbc.Button("Descargar el archivo de resultados en formato csv", 
                                    id="btn-descarga-resultados-sorteo-terrenos", 
                                    color="success", className="mr-1"), 

                            dcc.Download(id="descarga-resultado-sorteo-terrenos")
                        ],style={"display":'flex', "justify-content":"center", "align-items": "center"}),
                    ]),
                    
                ], style={'background-color':'#EBEBEB'}),
            ],
            id="descarga-resultado-sorteo-terrenos-modal",
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

# Tabla para mostrar La lista de los terrenos sin ganadores
tabla_ganadores_solo_terrenos = dash_table.DataTable(
    id='tabla-ganadores-solo-terrenos',
    columns=[{'name':['Terreno', 'No. Lote'], 'id':'numero_lote'},
             {'name':['Número ganador', 'Número'], 'id':'numero_ganador'},
             {'name':['Participante ganador', 'No. Empleado'], 'id':'num_empleado'}],
    merge_duplicate_headers=True,
    data=[],
    style_cell={
        'text_align':'center',
        'minWidth': 90, 'maxWidth': 90, 'width': 90,
        'whiteSpace': 'pre-line',
        'height': 'auto',
    },
    style_data={
        'whiteSpace': 'pre-line',
        'height': 'auto',
    },
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'text-align':'center',
    },
    fixed_rows={'headers': True},
    style_table={'height': 800},
)


# Tabla para mostrar a los ganadores de los terrenos
tabla_ganadores_terrenos = dash_table.DataTable(
    id='tabla-ganadores',
    columns=[{'name':['Terreno', 'No. Lote'], 'id':'numero_lote'},
             {'name':['Número ganador', 'Número'], 'id':'numero_ganador'},
             {'name':['Participante ganador', 'No. Empleado'], 'id':'num_empleado'},
            ],
    merge_duplicate_headers=True,
    data=[],
    style_cell={
        'text_align':'center',
        'minWidth': 90, 'maxWidth': 90, 'width': 90,
        'whiteSpace': 'pre-line',
        'height': 'auto',
    },
    style_data={
        'whiteSpace': 'pre-line',
        'height': 'auto',
    },
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'text-align':'center',
    },
    fixed_rows={'headers': True},
    style_table={'height': 800},
)

# Leyenda para la pila de boletos mezclados de la etapa 3
leyenda_pila_datos_etapa3 = html.Ul([
    html.Li([
        html.Span([
        ], style={'border':'3px solid #000000', 'float':'left', 'width':'20px', 'height':'20px', 
                  'margin':'2px', 'background-color':'#FFFFFF'}),
        
        html.H5('En juego', style={'float':'right'}),

    ], style={'float':'left', 'margin-right':'10px'}),

    html.Li([
        html.Span([
        ], style={'border':'3px solid #000000', 'float':'left', 'width':'20px', 'height':'20px', 
                  'margin':'2px', 'background-color':'#DE4B4B'}),

        html.H5('Retirados', style={'float':'right'}),

    ], style={'float':'left', 'margin-right':'10px'}),

    html.Li([
        html.Span([
        ], style={'border':'3px solid #000000', 'float':'left', 'width':'20px', 'height':'20px', 
                  'margin':'2px', 'background-color':'#0093E8'}),

        html.H5('Asignado al ganador actual', style={'float':'right'}),

    ], style={'float':'left', 'margin-right':'10px'}),

    html.Li([
        html.Span([
        ], style={'border':'3px solid #000000', 'float':'left', 'width':'20px', 'height':'20px', 
                  'margin':'2px', 'background-color':'#63CF55'}),

        html.H5('Ganador del lote actual', style={'float':'right'}),

    ], style={'float':'left', 'margin-right':'10px'})
], style={'list-style':'none'})


# -------------------------- OBJETOS DE LA ETAPA 4 ----------------------------

# Modal para pedir la semilla
semilla_modal_etapa4 = html.Div(
    [        
        dbc.Modal(
            [
                dbc.ModalHeader(html.H2("Establecer semilla para la definición de la lista de prelación"), style={'background-color':'#3D7EF2', 'color':'white'}),

                dbc.ModalBody(children=[
                    dbc.Form(id='semilla-modal-form-etapa4',
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
                        ],inline=True
                    ),
                    html.Div(
                    [
                        dbc.Button("Confirmar", id="ok-btn-modal-semilla-etapa4", color="success", 
                                style={'margin':"1em", 'float':'right'},)
                    ]
                    )
                ], style={'background-color':'#EBEBEB'},),
            ],
            id="semilla-modal-etapa4",
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

# Tabla para mostrar La lista de los terrenos sin ganadores
tabla_orden_prelacion = dash_table.DataTable(
    id='tabla-orden-prelacion',
    columns=[{'name':'Prioridad', 'id':'prioridad'},
             {'name':'No. Empleado', 'id':'num_empleado'}],
    merge_duplicate_headers=True,
    data=[],
    style_cell={
        'text_align':'center',
        'minWidth': 90, 'maxWidth': 90, 'width': 90,
        'whiteSpace': 'pre-line',
        'height': 'auto',
    },
    style_data={
        'whiteSpace': 'pre-line',
        'height': 'auto',
    },
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'text-align':'center',
    },
    fixed_rows={'headers': True},
    style_table={'height': 800},
)


# ***************************** PÁGINA PRINCIPAL ******************************

app.layout = html.Div([
    # ---------- OBJETOS DE ALMACENAMIENTO DE DATOS ----------

    # Objeto para almacenar la tabla de participantes de la etapa 1
    dcc.Store(
        id='info-tabla-participantes-etapa1', data=None
    ),

    # Objeto para almacenar el dataFrame de los terrenos
    dcc.Store(
        id='info-terrenos', data=None
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

    # Objeto para almacenar la semilla de la selección aleatoria de los terrenos
    dcc.Store(
        id='info-semilla-etapa3', data='Sin semilla'
    ),

    # Objeto para almacenar la asignación de boletos a los participantes
    dcc.Store(
        id='sorteo-boletos', data=None
    ),

    # Objeto para almacenar la asignación de terrenos a los participantes
    dcc.Store(
        id='info-sorteo-terrenos', data=None
    ),

    # Objeto para almacenar el siguiente participante a sortear
    dcc.Store(
        id='idx-participante-sorteo-boletos', data=0
    ),

    # Objeto para almacenar el siguiente terreno a sortear
    dcc.Store(
        id='idx-sorteo-terreno', data=0
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

    # Objeto para almacenar la bandera que nos indica si el modal para la descarga de los
    # resultados del sorteo de terrenos se abrirá o no
    dcc.Store(
        id='info-abrir-modal-descargar-resultados-sorteo-terrenos', data=False
    ),

    # Objeto para almacenar la bandera que nos indicará si el botón de sortear participante
    # se deshabilita o no
    dcc.Store(
        id='info-deshabilitar-boton-sortear-participante-boletos-no-mezclados', data=True
    ),

    dcc.Store(
        id='info-deshabilitar-boton-sortear-participante-sorteo-finalizado', data=True
    ),

    dcc.Store(
        id='info-habilitar-boton-sortear-participante-primer-participante', data=True
    ),

    dcc.Store(
        id='info-habilitar-boton-sortear-participante-siguiente-participante', data=True
    ),

    dcc.Store(
        id='info-deshabilitar-boton-sortear-terreno', data=True
    ),

    dcc.Store(
        id='info-habilitar-boton-sortear-terreno-primer-terreno', data=True
    ),

    dcc.Store(
        id='info-habilitar-boton-sortear-terreno-siguiente-terreno', data=True
    ),

    # Objeto para almacenar los boletos mezclados
    dcc.Store(
        id='info-boletos-mezclados', data=None
    ),

    # ----- Para la etapa 3 -----
    # Para almacenar los terrenos en la tabla de los ganadores
    dcc.Store(
        id='info-tabla-ganadores', data=None
    ),

    dcc.Store(
        id='info-tabla-ganadores2', data=None
    ),


    # ----- Para la etapa 4 -----
    # Para almacenar la semilla para definir el lista de prelación
    dcc.Store(
        id='info-semilla-etapa4', data='Sin semilla'
    ),

    dcc.Store(
        id='info-orden-prelacion', data=None
    ),


    # Modal para pedir una semilla
    semilla_modal_etapa2,
    

    # Objeto para la identificación de las rutas
    dcc.Location(id='url'),

    # Navbar de las etapas
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Etapa 1: Conteo de Números", href="/etapa1", id='link-etapa1')),
            dbc.NavItem(dbc.NavLink("Etapa 2: Asignación de Números", href="/etapa2", id='link-etapa2',
                                     disabled=True)),
            dbc.NavItem(dbc.NavLink("Etapa 3: Sorteo de Lotes", href="/etapa3", id='link-etapa3',
                                     disabled=True)),
            dbc.NavItem(dbc.NavLink("Etapa 4: Definición de la Lista de Prelación", href="/etapa4", id='link-etapa4',
                                     disabled=True)),
        ],
        brand="Etapas del Sorteo",
        brand_href="/",
        color="primary",
        dark=True,
    ),

    #  ------------------ CONTENIDO PRINCIPAL DE LA PÁGINA --------------------

    # "Landing page"
    html.Div(id='div-principal', children=[
        html.H3("¡BIENVENIDOS Y MUCHA SUERTE!",style={'text-align':'center', 'padding':'1em'}),
    ]),


    # -------------------------------- Etapa 1 ---------------------------------
    html.Div(id='div-etapa1', children=[
        html.Div(children=[
            html.H1("ETAPA 1: CONTEO DE NÚMEROS",style={'text-align':'center', 'padding':'1em'}),
        ]),

        html.H3('TABLA DE PARTICIPANTES', style={'text-align':'center', 'padding':'1em'}),
        
        tabla_participantes_etapa1,
        
        html.Br(),
        html.Br(),
        
        html.Br(),
        dbc.Label(html.H3("Número de participantes: ")),
        dbc.Label(html.H3("", id='total-participantes-label'), style={'padding':'1em'}),

        html.Br(),
        dbc.Label(html.H3("Total de números: ")),
        dbc.Label(html.H3("", id='total-boletos-label'), style={'padding':'1em'}),
        

        dbc.Row([
            html.Div([
                html.H3('NÚMEROS PARTICIPANTES EN EL SORTEO', style={'text-align':'center', 'padding':'1em'}),
                
            ], style={"margin": "auto","width": "85%", 'padding':'1em'}),
            
            html.Div([
            ], style={"position":"relative", "height":"800px", "overflow":"auto", "display":"block", "justify":"center"}, id='div-pila-datos-etapa1'),
        ])
    ], style={"margin": "auto","width": "100%", 'padding':'1em', 'display':'none'}),

    # -------------------------------- Etapa 2 ---------------------------------

    html.Div(id='div-etapa2', children=[
        # Modal para descargar el resultado del sorteo de los boletos
        descarga_resultados_sorteo_boletos_modal,

        # Modal de confirmación cuando el sorteo se realice
        afirmacion_sorteo_boletos_modal_etapa2, 

        html.Div(children=[
            html.H1("ETAPA 2: ASIGNACIÓN DE NÚMEROS",style={'text-align':'center', 'padding':'1em'}),
        ]),

        html.Div([
            html.H4([
                "Los resultados se publicarán en la siguiente página: ",
                dcc.Link(
                    href="https://diyecora.unison.mx/sorteo13lotes",
                    target='blank'
                ),
            ],style={'text-align':'center'}),
        ], id='link-resultados-etapa2', style={'display':'none'}),
        
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
                    dbc.Button("Mezclar números", id="sorteo-boletos-btn", 
                               color="success", className="mr-1", style={'margin-left':'15px'})
                ],style={'text-align':'left', 'margin':'auto'}),
                

                html.Div([
                    html.H3('PARTICIPANTES CON NÚMEROS ASIGNADOS', style={'text-align':'center', 'padding':'1em'}),
                    
                    tabla_participantes_etapa2,
                    
                ], style={"margin": "auto","width": "85%", 'padding':'1em'})
            ],md=6),

            dbc.Col([
                html.Div([
                    html.H3('PARTICIPANTE ACTUAL', style={'text-align':'center'}),
                    
                    tabla_sorteo_etapa2,

                    html.H3('LISTA DE NÚMEROS ASIGNADOS AL PARTICIPANTE ACTUAL', style={'text-align':'center'}),

                    tabla_boletos_etapa2,

                    html.Br(),
                    html.H3(children=[], style={'text-align':'right'}, 
                            id='participantes-restantes-label'),
                    html.Br(),

                    dbc.Button("Los números no se han mezclado", id="siguiente-btn", color="primary", className="mr-1", style={'float':'right'}, disabled=True),
                    
                ], style={"margin": "auto","width": "85%", 'padding':'1em'})
            ],md=6)
            
        ]),
        
        html.Div([
            html.H3('NÚMEROS PARTICIPANTES EN EL SORTEO', style={'text-align':'center', 'padding':'1em'}), 
        ], style={"margin": "auto","width": "85%", 'padding':'1em'}),

        html.Div([
            leyenda_pila_datos_etapa2
        ], style={'margin-left':'auto', 'padding':'1em'}),
        
        html.Div([
        ], style={"position":"relative", "height":"800px", "overflow":"auto", "display":"block", "justify":"center", "margin": "0 auto", "width": "95%"}, id='div-pila-datos-etapa2'),
 

    ], style={'display':"none"}),

    # -------------------------------- Etapa 3 ---------------------------------
    
    html.Div(id='div-etapa3', children=[
        html.Div(children=[
            html.H1("ETAPA 3: SORTEO DE LOTES",style={'text-align':'center', 'padding':'1em'}),
        ]),

        html.Div([
            html.H4([
                "Los resultados se publicarán en la siguiente página: ",
                dcc.Link(
                    href="https://diyecora.unison.mx/sorteo13lotes",
                    target='blank'
                ),
            ],style={'text-align':'center'}),
        ], id='link-resultados-etapa3', style={'display':'none'}),

        # Modal para establecer una semilla para el sorteo de los terrenos
        semilla_modal_etapa3,

        # Modal para descargar el resultado del sorteo de los terrenos
        descarga_resultados_sorteo_terrenos_modal,
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Label(html.H3("Semilla: Sin semilla", id='label-semilla-etapa3'), 
                          style={'text-align':'center', 'padding':'1em'})
                ],style={'text-align':'left', 'margin':'auto'}),
                

                html.Div([
                    html.H3('GANADORES', style={'text-align':'center', 'padding':'1em'}),
                    
                    html.Div([
                        tabla_ganadores_terrenos,    
                    ], id="div-tabla-ganadores", style={'display':'none'}),

                    html.Div([
                        tabla_ganadores_solo_terrenos,    
                    ], id="div-tabla-ganadores-solo-terrenos"),
                    
                ], style={"margin": "auto","width": "85%", 'padding':'1em'})
            ],md=6),

            dbc.Col([
                html.Div([
                    html.H3('NÚMERO DEL LOTE ACTUAL', style={'text-align':'center'}),

                    html.H3(children=[], style={'text-align':'center'}, 
                            id='terreno-actual-label'),
                    
                    html.Br(),

                    html.H3('NÚMERO GANADOR', style={'text-align':'center'}),
                    html.H3(children=[], style={'text-align':'center'}, 
                            id='boleto-ganador-label'),
                    
                    html.Br(),

                    html.H3('NÚMERO DE EMPLEADO DEL PARTICIPANTE GANADOR', style={'text-align':'center'}),

                    html.Br(),
                    html.H3(children=[], style={'text-align':'center'}, 
                            id='participante-ganador-label'),

                    html.Br(),
                    html.H3(children=[], style={'text-align':'right'}, 
                            id='terrenos-restantes-label'),
                    dbc.Button("Comenzar el sorteo de los lotes", id="siguiente-terreno-btn", color="primary", className="mr-1", style={'float':'right'}),

                    
                ], style={"margin": "auto","width": "85%", 'padding':'1em'})
            ],md=6)
            
        ]),
        
        html.Div([
            html.H3('NÚMEROS PARTICIPANTES EN EL SORTEO', style={'text-align':'center', 'padding':'1em'}),
            
        ], style={"margin": "auto","width": "85%", 'padding':'1em'}),

        html.Div([
            leyenda_pila_datos_etapa3
        ], style={'margin-left':'auto', 'padding':'1em'}),
        
        html.Div([
        ], style={"position":"relative", "height":"800px", "overflow":"auto", "display":"block", "justify":"center", "margin": "0 auto", "width": "95%"}, id='div-pila-datos-etapa3'),
 

    ], style={'display':"none"}),

    # -------------------------------- Etapa 4 ---------------------------------

    html.Div(id='div-etapa4', children=[
        
        semilla_modal_etapa4,
  
        html.Div(children=[
            html.H1("ETAPA 4: DEFINICIÓN DE LA LISTA DE PRELACIÓN",style={'text-align':'center', 'padding':'1em'}),
        ]),

        html.Div([
            html.H4([
                "Los resultados se publicarán en la siguiente página: ",
                dcc.Link(
                    href="https://diyecora.unison.mx/sorteo13lotes",
                    target='blank'
                ),
            ],style={'text-align':'center'}),
        ], id='link-resultados-etapa4', style={'display':'none'}),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Label(html.H3("Semilla: Sin semilla", id='label-semilla-etapa4'), 
                          style={'text-align':'center', 'padding':'1em'}),
                    html.Br(),
                    dbc.Button("Mezclar participantes no ganadores", id="sorteo-prelacion-btn", 
                               color="success", className="mr-1", style={'margin-left':'15px'})
                ],style={'text-align':'left', 'margin':'auto'}),
            ],md=6),
            
        ]),
        
        html.Div([
            html.H3('LISTA DE PRELACIÓN', style={'text-align':'center', 'padding':'1em'}), 
            tabla_orden_prelacion,
        ], style={"margin": "auto","width": "50%", 'padding':'1em'}),

        html.Div([
            #dbc.Button("Descargar lista de prelación", id="descargar-orden-prelacion-btn", color="primary", className="mr-1", style={'float':'right'}),
            dbc.Button("La lista de prelación no se ha calculado", id="descargar-orden-prelacion-btn", disabled=True, color="primary", className="mr-1", style={'float':'right'}),
            dcc.Download(id="descarga-resultado-orden-prelacion")
        ], style={"margin": "auto","width": "55%", 'padding':'1em'}),

        

    ], style={'display':"none"}),
])




# ********************************* CALLBACKS *********************************

# ----> Callback para actualizar el contenido de la página i.e. el cambio de
#       etapa ocultando o mostrando elementos 
@app.callback(
    [Output('div-principal', 'style'), Output('div-etapa1', 'style'), Output('div-etapa2', 'style'),
     Output('div-etapa3', 'style'), Output('div-etapa4', 'style'), Output('link-etapa1', 'style'), 
     Output('link-etapa2', 'style'), Output('link-etapa3', 'style'), Output('link-etapa4', 'style')],
    Input('url', 'pathname')
)
def cambiarEtapa(url):
    if url == '/':
        return {}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {}, {}, {}, {}
    if url == '/etapa1':
        return {'display':'none'}, {"margin": "auto","width": "85%", 'padding':'1em'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {"font-weight": "1000", 'color':'white'}, {}, {}, {}
    elif url == '/etapa2':
        return {'display':'none'}, {'display':'none'}, {}, {'display':'none'}, {'display':'none'}, {}, {"font-weight": "1000", 'color':'white'}, {}, {}
    elif url == '/etapa3':
        return {'display':'none'}, {'display':'none'}, {'display':'none'}, {}, {'display':'none'}, {}, {}, {"font-weight": "1000", 'color':'white'}, {}
    elif url == '/etapa4':
        return {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {}, {}, {}, {}, {"font-weight": "1000", 'color':'white'}

    # Objeto para almacenar las columnas de la tabla de la pila de boletos
    dcc.Store(
        id='info-columnas-tabla-pila-boletos', data=None
    ),



# *************************** CALLBACKS DE LA ETAPA 1 **************************

# ----> Callback para crear la tabla de los participante, calcular el total de
#       participantes y boletos, y guardarlos. Además, se crea la pila de boletos
#       ordenada.
@app.callback(
    [Output('tabla-participantes-etapa1', 'data'), Output('info-tabla-participantes-etapa1', 'data'),
     Output('total-participantes-label', 'children'), Output('total-boletos-label', 'children'),
     Output('info-total-participantes', 'data'), Output('info-total-boletos', 'data'),
     Output('div-pila-datos-etapa1', 'children'), Output('info-terrenos', 'data'),
     Output('link-etapa2', 'disabled')],

    Input('link-etapa1', 'n_clicks'),

    [State('info-tabla-participantes-etapa1', 'data'), State('info-total-participantes', 'data'), 
     State('info-total-boletos', 'data'), State('info-num-columnas-pila-boletos', 'data'),
     State('div-pila-datos-etapa1', 'children')],
)
def mostrarInfoEtapa1(link_etapa1, tabla_participantes_etapa1, total_participantes, total_boletos, 
                     n_cols, pila_datos_children):
    if link_etapa1:
        # Si no tenemos una tabla, entonces la creamos y calculamos los totales de boletos y
        # participantes
        if not tabla_participantes_etapa1 and not total_participantes and not total_boletos:
            print("NO HAY NADA, SE VA A CALCULAR TODO")
            # ----- Creación del DataFrame de los participantes -----
            df_participantes = pd.read_csv('./datos/PARTICIPANTES SORTEO 13 LOTES UNISON 31 de mayo de 2021.csv')
            df_participantes.columns = ['num_empleado', 'antiguedad']
            df_participantes = df_participantes[['num_empleado', 'antiguedad']]
            df_participantes = df_participantes.sort_values(by=['antiguedad'], ascending=[False])
            print(df_participantes)
            
            # ----- Creación del DataFrame de los terrenos -----
            df_terrenos = pd.read_csv('./datos/LOTES.csv')

            # Se calcula el total de participantes y el total de los boletos
            n_participantes = len(df_participantes.index)
            n_boletos = int(df_participantes['antiguedad'].sum())

            # Se formatea la información del DataFrame de los participantes
            data_participantes = df_participantes.to_dict('records')

            # Se formatea la información del DataFrame de los terrenos
            data_terrenos = df_terrenos.to_dict('records')
            print("TERRENOS")
            print(data_terrenos)

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


            return data_participantes, data_participantes, n_participantes, n_boletos, n_participantes, n_boletos, table, data_terrenos, False
        else:
            print("YA EXISTE TODO, SE VA A ENVIAR DIRECTAMENTE")
            return dash.no_update
    else:
        return dash.no_update



# *************************** CALLBACKS DE LA ETAPA 2 **************************

# ----> Callback para revisar si es necesario introducir una nueva semilla para
#       el sorteo de los boletos
@app.callback(
    Output('semilla-modal', 'is_open'),
    [Input('link-etapa2', 'n_clicks'), Input('ok-btn-modal-semilla', 'n_clicks')],
    [State('semilla-modal', 'is_open'), State('info-semilla', 'data')]
)
def mostrarModalSemilla(link_etapa2, ok_btn_modal_semilla, modal_esta_abierto, info_semilla):
    contexto = dash.callback_context
    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        boton = contexto.triggered[0]['prop_id'].split('.')[0]

        if boton == 'link-etapa2':
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
    [Input('link-etapa2', 'n_clicks'), Input('ok-btn-modal-semilla', 'n_clicks')],
    [State('semilla-modal-form', 'children'), State('info-semilla', 'data')]
)
def actualizarSemilla(link_etapa2, ok_btn_modal_semilla, modal_childrens, info_semilla):

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

            semilla = f"{dia.zfill(2)}/{mes.zfill(2)}/{anio} {hora.zfill(2)}:{minuto.zfill(2)}"
            semilla_label = "Semilla: " + semilla

            return semilla_label, semilla
        elif boton == 'link-etapa2':
            print("se mantiene la semilla")
            return dash.no_update
    else:
        return dash.no_update

# ----> Callback para realizar el sorteo de los boletos y notificar que se
#       realizó exitosamente. Además, se crea la pila de boletos mezclados. También se habilita
#       el botón para sortear participantes
@app.callback(
    [Output('afirmacion-sorteo-boletos-modal', 'is_open'), Output('sorteo-boletos', 'data'),
     Output('div-pila-datos-etapa2', 'children'), Output('sorteo-boletos-btn', 'disabled'),
     Output('sorteo-boletos-btn', 'children'), Output('info-habilitar-boton-sortear-participante-primer-participante', 'data'),
     Output('div-pila-datos-etapa3', 'children'),
     Output('info-boletos-mezclados', 'data')],

    [Input('sorteo-boletos-btn', 'n_clicks'), Input('ok-afirmacion-sorteo-boletos-btn-modal', 'n_clicks')],

    [State('info-semilla', 'data'), State('sorteo-boletos', 'data'), 
     State('info-tabla-participantes-etapa1', 'data'), State('info-num-columnas-pila-boletos', 'data'),
     State('div-pila-datos-etapa2', 'children'), State('info-sorteo-terrenos', 'data'),
     State('info-terrenos', 'data'), State('info-boletos-mezclados', 'data'), 
     State('div-pila-datos-etapa3', 'children')]

)
def sortearBoletos(sorteo_boletos_btn, ok_btn_sorteo_boletos_modal, info_semilla, sorteo_boletos,
                   info_tabla_participantes, n_cols, pila_datos_children, info_sorteo_terrenos, 
                   info_terrenos, info_boletos_mezclados, pila_datos_etapa3):
    contexto = dash.callback_context

    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        boton = contexto.triggered[0]['prop_id'].split('.')[0]

        if boton == 'sorteo-boletos-btn':
            # Se obtiene el DataFrame de la etapa anterior
            df_participantes = pd.DataFrame.from_dict(info_tabla_participantes)
            # Se realiza el sorteo de los boletos con la semilla dada.
            df_sorteo, pila_boletos_mezclados = sorteoNumeros(df_participantes, info_semilla)
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
            table_pila_boletos_etapa2 = dbc.Table(table_body, bordered=True, id='tabla-pila-boletos-etapa2')
            table_pila_boletos_etapa3 = dbc.Table(table_body, bordered=True, id='tabla-pila-boletos-etapa3')

            return True, df_sorteo.to_dict('records'), table_pila_boletos_etapa2, True, "Los números ya se han mezclado", True, table_pila_boletos_etapa3, pila_boletos_mezclados
        elif boton == 'ok-afirmacion-sorteo-boletos-btn-modal':
            print("OK")
            return False, sorteo_boletos, pila_datos_children, True, "Los números ya se han mezclado", True, pila_datos_etapa3, info_boletos_mezclados
    else:
        return dash.no_update

# ----> Callback para la visualización del sorteo de los boletos
@app.callback(
    [Output('tabla-participantes-etapa2', 'data'), Output('idx-participante-sorteo-boletos', 'data'),
     Output('tabla-participante-actual', 'data'), Output('tabla-boletos-participante-actual', 'data'),
     Output('tabla-pila-boletos-etapa2', 'children'), Output('participantes-restantes-label', 'children'), 
     Output('info-abrir-modal-descargar-resultados-sorteo-boletos', 'data'),
     Output('info-deshabilitar-boton-sortear-participante-sorteo-finalizado', 'data'), 
     Output('info-habilitar-boton-sortear-terreno-primer-terreno', 'data'), Output('link-etapa3', 'disabled')],

    Input('siguiente-btn', 'n_clicks'),

    [State('idx-participante-sorteo-boletos', 'data'), State('sorteo-boletos', 'data'),
     State('tabla-participantes-etapa2','data'), State('info-num-columnas-pila-boletos', 'data'),
     State('tabla-pila-boletos-etapa2', 'children'), State('info-total-participantes', 'data')],
     prevent_initial_call=True
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
        for boleto in participante_actual['numeros']:
            str_boletos += boleto + ", "
            
        

        # Se crea su registro en la tabla de Participantes con Boleto y se agrega
        registro_participantes_con_boleto = {'num_empleado':participante_actual['num_empleado'],
                                             'antiguedad':participante_actual['antiguedad'],
                                             'numeros':str_boletos[:-2]}
        datos_tabla_participantes.append(registro_participantes_con_boleto)
        
        # Se crea su registro en la tabla de Participante Sorteado
        registro_participante_sorteado = [{'num_empleado':participante_actual['num_empleado'],
                                           'antiguedad':participante_actual['antiguedad']}]
        
        # Se crea el registro con la lista de los boletos para añadirla a la lista de sus boletos
        registro_tabla_boletos = [{'numeros':str_boletos[:-2]}]

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
                if casilla['props']['children'] in participante_actual['numeros']:
                    casilla['props']['style']['background-color'] = '#0093E8'
                    casilla['props']['style']['color'] = '#FFFFFF'
        
        # Se crea una nueva etiqueta para indicar a los participantes restantes
        etiqueta_participantes_restantes = f"({total_participantes-idx_participante-1} restantes)"

        # Se decide si ya es necesario bloquear el botón de "siguiente participante"
        abrir_modal_descarga_resultados = False
        deshabilitar_boton_sortear_participante = False
        habilitar_sorteo_terrenos = False
        habilitar_etapa3 = True
        if idx_participante == total_participantes - 1:
            print("SE ACABA DE SORTEAR EL ÚLTIMO PARTICIPANTE")
            abrir_modal_descarga_resultados = True
            deshabilitar_boton_sortear_participante = True
            habilitar_sorteo_terrenos = True
            habilitar_etapa3 = False

        return datos_tabla_participantes, idx_participante+1, registro_participante_sorteado, registro_tabla_boletos, pila_datos_children, etiqueta_participantes_restantes, abrir_modal_descarga_resultados, deshabilitar_boton_sortear_participante, habilitar_sorteo_terrenos, habilitar_etapa3
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
                time.sleep(10)
                return True
        elif elemento == 'btn-descarga-resultados-sorteo-boletos':
            return not modal_esta_abierto
    else:
        return modal_esta_abierto


# Callback para bloquear, el botón de sortear boletos a los participantes cuando este sorteo
# termine
@app.callback(
    [Output('siguiente-btn', 'disabled'), Output('siguiente-btn', 'children')],
    [Input('info-deshabilitar-boton-sortear-participante-sorteo-finalizado', 'data'),
     Input('info-habilitar-boton-sortear-participante-primer-participante', 'data'),
     Input('info-habilitar-boton-sortear-participante-siguiente-participante', 'data')]
)
def deshabilitarBotonSortearSiguienteParticipante(deshabilitar_sorteo_finalizado, 
                                                  habilitar_primer_participante,
                                                  habilitar_siguiente_participante):
    contexto = dash.callback_context
    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        boton = contexto.triggered[0]['prop_id'].split('.')[0]

        if boton == 'info-deshabilitar-boton-sortear-participante-sorteo-finalizado':
            if deshabilitar_sorteo_finalizado:
                return True, "Asignación de números finalizada"
            else:
                return False, "Asignar números al siguiente participante"

        elif boton == 'info-habilitar-boton-sortear-participante-primer-participante':
            return False, "Comenzar la asignación de números"
        elif boton == 'info-habilitar-boton-sortear-participante-siguiente-participante':
            return False, "Asignar números al siguiente participante"
    else:
        return dash.no_update

# Callback para descargar los resultados del sorteo de boletos
@app.callback(
    [Output('descarga-resultado-sorteo-boletos', 'data'), Output('link-resultados-etapa2', 'style')],
    Input('btn-descarga-resultados-sorteo-boletos', 'n_clicks'),
    State('sorteo-boletos', 'data'),
    prevent_initial_call=True
)
def descargarResultadoAsignacionBoletos(btn_descarga_resultados, diccionario_resultados_sorteo_boletos): 
    texto = "# Listado de números asignados a empleados de confianza que participarán en el\n# \"Sorteo de Trece Lotes del Fraccionamiento Villa Universitaria\"\n\n"
    texto += pd.DataFrame.from_dict(diccionario_resultados_sorteo_boletos).to_csv(index=False)
    return dict(content=texto,filename="ASIGNACION_DE_NUMEROS.csv"), {}



# *************************** CALLBACKS DE LA ETAPA 3 **************************
# ----> Callback para revisar si es necesario introducir una nueva semilla para
#       el sorteo de los terrenos
@app.callback(
    Output('semilla-modal-etapa3', 'is_open'),
    [Input('link-etapa3', 'n_clicks'), Input('ok-btn-modal-semilla-etapa3', 'n_clicks')],
    [State('semilla-modal-etapa3', 'is_open'), State('info-semilla-etapa3', 'data')]
)
def mostrarModalSemilla(link_etapa3, ok_btn_modal_semilla, modal_esta_abierto, info_semilla):
    contexto = dash.callback_context
    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        boton = contexto.triggered[0]['prop_id'].split('.')[0]

        if boton == 'link-etapa3':
            if info_semilla == 'Sin semilla':
                print("Se necesita una nueva semilla para el sorteo de los terrenos")
                return not modal_esta_abierto
        elif boton == 'ok-boton-modal-semilla-etapa3':
            print("Se cierra el modal")
            return not modal_esta_abierto
    else:
        return modal_esta_abierto

# ----> Callback para leer la semilla del modal y actualizarla en el objeto
#       dcc.Store y en su correspondiente etiqueta.
@app.callback(
    [Output('tabla-ganadores-solo-terrenos', 'data'), Output('label-semilla-etapa3', 'children'), 
     Output('info-semilla-etapa3', 'data'), Output('info-sorteo-terrenos', 'data'),
     Output('info-tabla-ganadores', 'data')],

    [Input('link-etapa3', 'n_clicks'), Input('ok-btn-modal-semilla-etapa3', 'n_clicks')],

    [State('semilla-modal-form-etapa3', 'children'), State('info-semilla-etapa3', 'data'),
     State('sorteo-boletos', 'data'), State('info-terrenos', 'data'), 
     State('info-boletos-mezclados', 'data')]
)
def actualizarSemilla(link_etapa3, ok_btn_modal_semilla, modal_childrens, info_semilla,
                      sorteo_boletos_data, info_terrenos, pila_boletos_mezclados):

    contexto = dash.callback_context
    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        boton = contexto.triggered[0]['prop_id'].split('.')[0]

        if boton == 'ok-btn-modal-semilla-etapa3':
            print("Leyendo la semilla de la etapa 3...")
            # Se obtiene la semilla introducida
            dia = modal_childrens[0]['props']['children'][1]['props']['value']
            mes = modal_childrens[1]['props']['children'][1]['props']['value']
            anio = modal_childrens[2]['props']['children'][1]['props']['value']
            hora = modal_childrens[3]['props']['children'][1]['props']['value']
            minuto = modal_childrens[4]['props']['children'][1]['props']['value']

            semilla = f"{dia.zfill(2)}/{mes.zfill(2)}/{anio} {hora.zfill(2)}:{minuto.zfill(2)}"
            semilla_label = "Semilla: " + semilla

            # Se obtiene el DataFrame de los terrenos
            df_terrenos = pd.DataFrame.from_dict(info_terrenos)

            # Se realiza el sorteo de los terrenos con la semilla dada
            df_sorteo_terrenos = sorteoLotes(semilla, pd.DataFrame.from_dict(sorteo_boletos_data), df_terrenos, pila_boletos_mezclados)

            # Se crea la tabla vacía de los ganadores
            # Se extraen los números de lote del terreno porque es lo único que nos interesa
            num_lotes = df_sorteo_terrenos['Numero_Lote']

            # Se generan los registros en blanco para la tabla de ganadores
            data_tabla_ganadores = []
            for num_lote in num_lotes:
                registro = {'numero_lote':num_lote,
                            'numero_ganador': " ",
                            'num_empleado': " "}
                data_tabla_ganadores.append(registro)

            return data_tabla_ganadores, semilla_label, semilla, df_sorteo_terrenos.to_dict('records'), data_tabla_ganadores

        elif boton == 'link-etapa3':
            print("se mantiene la semilla")
            return dash.no_update
    else:
        return dash.no_update

# ----> Callback para crear la tabla de ganadores vacía
@app.callback(
    [Output('tabla-ganadores', 'data'), Output('idx-sorteo-terreno', 'data'),
     Output('participante-ganador-label', 'children'), Output('tabla-pila-boletos-etapa3', 'children'), 
     Output('terreno-actual-label', 'children'),
     Output('boleto-ganador-label', 'children'), Output('terrenos-restantes-label', 'children'),
     Output('info-abrir-modal-descargar-resultados-sorteo-terrenos', 'data'),
     Output('div-tabla-ganadores', 'style'), Output('div-tabla-ganadores-solo-terrenos', 'style'),
     Output('info-tabla-ganadores2', 'data'),
     Output('info-deshabilitar-boton-sortear-terreno','data'), Output('link-etapa4', 'disabled')],

    Input('siguiente-terreno-btn', 'n_clicks'),

    [State('info-sorteo-terrenos', 'data'),
     State('idx-sorteo-terreno', 'data'), State('participante-ganador-label', 'children'),
     State('tabla-pila-boletos-etapa3', 'children'), 
     State('terreno-actual-label', 'children'),
     State('boleto-ganador-label', 'children'), State('terrenos-restantes-label', 'children'),
     State('info-tabla-ganadores', 'data'), State('info-tabla-ganadores2', 'data')],
    prevent_initial_call=True
)
def sortearGanadores(siguiente_terreno_btn, sorteo_terrenos_data, 
                     idx_terreno, tabla_participante_ganador_data, pila_boletos_children, terreno_actual_label,
                     boleto_ganador_label, terrenos_restantes_label, tabla_ganadores_data1,
                     tabla_ganadores_data2):
    contexto = dash.callback_context
    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        boton = contexto.triggered[0]['prop_id'].split('.')[0]
        
        # Caso en donde sorteamos un nuevo terreno
        if boton == 'siguiente-terreno-btn':
            # Se obtiene el dataframe del sorteo de los terrenos
            df_sorteo_terrenos = pd.DataFrame.from_dict(sorteo_terrenos_data)

            # Se extrae el terreno actual
            terreno_actual = df_sorteo_terrenos.to_dict('records')[idx_terreno]

            # Se crea el registro en la tabla de los ganadores
            registro_tabla_ganadores = {'numero_lote':terreno_actual['Numero_Lote'],
                                        'numero_ganador':terreno_actual['numero_ganador'],
                                        'num_empleado':terreno_actual['num_empleado']}
            
            # Se reemplaza el registro del terreno correspondiente en el cuerpo de la tabla de
            # ganadores
            if idx_terreno == 0:
                tabla_ganadores_data = tabla_ganadores_data1
            else:
                tabla_ganadores_data = tabla_ganadores_data2
            
            tabla_ganadores_data[idx_terreno] = registro_tabla_ganadores


            # Se crea el registro del ganador en la tabla del ganador actual
            tabla_participante_ganador_data = html.H3(terreno_actual['num_empleado'], style={"border": "1px solid #ccc"})
            
            # En la pila de boletos en juego, se marca en azul el boleto ganador y en rojo los
            # demás boletos del ganador actual y el de los anteriores
            for renglon in pila_boletos_children['props']['children']:
                for casilla in renglon['props']['children']:
                    # Se les cambia el color a los boletos ya seleccionados (rojo)
                    try:
                        if (casilla['props']['style']['background-color'] == '#0093E8' 
                        or casilla['props']['style']['background-color'] == '#63CF55'):
                            casilla['props']['style']['background-color'] = '#DE4B4B'
                    except:
                        pass

                    # Se ponen en azul todos los boletos del participante actual y en verde
                    # el boleto ganador
                    if casilla['props']['children'] in terreno_actual['numeros']:
                        if casilla['props']['children'] != terreno_actual['numero_ganador']:
                            casilla['props']['style']['background-color'] = '#0093E8'
                            casilla['props']['style']['color'] = '#FFFFFF'
                        else:
                            casilla['props']['style']['background-color'] = '#63CF55'
                            casilla['props']['style']['color'] = '#FFFFFF'
            

            # Se crea la etiqueta para el terreno actual
            terreno_actual_label = html.H3(terreno_actual['Numero_Lote'], style={"border": "1px solid #ccc"})

            # Se crea la etiqueta para el boleto ganador actual
            boleto_ganador_label = html.H3(terreno_actual['numero_ganador'], style={"border": "1px solid #ccc"})

            # Se crea la etiqueta para los terrenos restantes 
            terrenos_restantes_label = html.H3(f"({len(df_sorteo_terrenos)-idx_terreno-1} restantes)")

            # Se decide si ya es necesario bloquear el botón de "siguiente participante"
            abrir_modal_descarga_resultados = False
            deshabilitar_boton_sortear_terreno = False
            deshabilitar_etapa4 = True
            if idx_terreno == len(df_sorteo_terrenos)- 1:
                print("SE ACABA DE SORTEAR EL ULTIMO TERRENO")
                abrir_modal_descarga_resultados = True
                deshabilitar_boton_sortear_terreno = True
                deshabilitar_etapa4 = False

            return tabla_ganadores_data, idx_terreno+1, tabla_participante_ganador_data, pila_boletos_children, terreno_actual_label, boleto_ganador_label, terrenos_restantes_label, abrir_modal_descarga_resultados, {}, {'display':'none'}, tabla_ganadores_data, deshabilitar_boton_sortear_terreno, deshabilitar_etapa4
        else:
            return dash.no_update

# Callback para desplegar, en caso de ser necesario, el modal para descargar los resultados del
# sorteo de boletos
@app.callback(
    Output("descarga-resultado-sorteo-terrenos-modal", 'is_open'),
    [Input('info-abrir-modal-descargar-resultados-sorteo-terrenos', 'data'),
     Input("btn-descarga-resultados-sorteo-terrenos", 'n_clicks')],
    State("descarga-resultado-sorteo-terrenos-modal", 'is_open')
)
def mostrarModalDescargaResultadosSorteoBoletos(info_abrir_modal, btn_descarga, modal_esta_abierto):
    contexto = dash.callback_context
    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        elemento = contexto.triggered[0]['prop_id'].split('.')[0]
        if elemento == "info-abrir-modal-descargar-resultados-sorteo-terrenos":
            if info_abrir_modal:
                time.sleep(10)
                return True
        elif elemento == 'btn-descarga-resultados-sorteo-terrenos':
            return not modal_esta_abierto
    else:
        return modal_esta_abierto

# Callback para bloquear, el botón de sortear terrenos cuando este sorteo termine
@app.callback(
    [Output('siguiente-terreno-btn', 'disabled'), Output('siguiente-terreno-btn', 'children')],
    [Input('info-deshabilitar-boton-sortear-terreno', 'data')],
     prevent_initial_call=True
)
def deshabilitarBotonSortearSiguienteBoleto(deshabilitar):
    contexto = dash.callback_context
    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        boton = contexto.triggered[0]['prop_id'].split('.')[0]

        if boton == 'info-deshabilitar-boton-sortear-terreno':
            if deshabilitar:
                return True, "Sorteo finalizado"
            else:
                return False, "Sortear el siguiente lote"

    else:
        return dash.no_update

# Callback para descargar los resultados del sorteo de terrenos
@app.callback(
    [Output('descarga-resultado-sorteo-terrenos', 'data'), Output('link-resultados-etapa3', 'style')],
    Input('btn-descarga-resultados-sorteo-terrenos', 'n_clicks'),
    State('info-sorteo-terrenos', 'data'),
    prevent_initial_call=True
)
def descargarResultadoGanadores(btn_descarga_resultados, diccionario_resultados_sorteo_terrenos): 
    df = pd.DataFrame.from_dict(diccionario_resultados_sorteo_terrenos)
    df['numero_ganador'] = [f"\'{b}\'" for b in df['numero_ganador']]
    df = df.drop(columns=['antiguedad', 'numeros']).to_csv(index=False)

    texto = "# Resultado de ganadores en el \n# \"Sorteo de Trece Lotes del Fraccionamiento Villa Universitaria\" \n\n"
    texto += df
    
    return dict(content=texto, filename="RESULTADOS_DEL_SORTEO.csv"), {}


# *************************** CALLBACKS DE LA ETAPA 4 **************************
# ----> Callback para revisar si es necesario introducir una nueva semilla para
#       asignar el lista de prelación
@app.callback(
    Output('semilla-modal-etapa4', 'is_open'),
    [Input('link-etapa4', 'n_clicks'), Input('ok-btn-modal-semilla-etapa4', 'n_clicks')],
    [State('semilla-modal-etapa4', 'is_open'), State('info-semilla-etapa4', 'data')],

    prevent_initial_call=True
)
def mostrarModalSemillaOrdenPrelacion(link_etapa4, ok_btn_modal_semilla, modal_esta_abierto, info_semilla):
    contexto = dash.callback_context
    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        boton = contexto.triggered[0]['prop_id'].split('.')[0]

        if boton == 'link-etapa4':
            if info_semilla == 'Sin semilla':
                print("Se necesita una nueva semilla para el lista de prelación")
                return not modal_esta_abierto
        elif boton == 'ok-boton-modal-semilla-etapa4':
            print("Se cierra el modal de la semilla del lista de prelación")
            return not modal_esta_abierto
    else:
        return modal_esta_abierto

# ----> Callback para leer la semilla del modal y actualizarla en el objeto
#       dcc.Store y en su correspondiente etiqueta.
@app.callback(
    [Output('label-semilla-etapa4', 'children'), Output('info-semilla-etapa4', 'data')],

    [Input('link-etapa4', 'n_clicks'), Input('ok-btn-modal-semilla-etapa4', 'n_clicks')],

    State('semilla-modal-form-etapa4', 'children'), 

    prevent_initial_call=True
)
def actualizarSemillaOrdenPrelacion(link_etapa4, ok_btn_modal_semilla, modal_childrens):

    contexto = dash.callback_context
    if contexto.triggered:
        # Se busca qué elemento disparó el callback
        boton = contexto.triggered[0]['prop_id'].split('.')[0]

        if boton == 'ok-btn-modal-semilla-etapa4':
            print("Leyendo la semilla de la etapa 4...")
            # Se obtiene la semilla introducida
            dia = modal_childrens[0]['props']['children'][1]['props']['value']
            mes = modal_childrens[1]['props']['children'][1]['props']['value']
            anio = modal_childrens[2]['props']['children'][1]['props']['value']
            hora = modal_childrens[3]['props']['children'][1]['props']['value']
            minuto = modal_childrens[4]['props']['children'][1]['props']['value']

            semilla = f"{dia.zfill(2)}/{mes.zfill(2)}/{anio} {hora.zfill(2)}:{minuto.zfill(2)}"
            semilla_label = "Semilla: " + semilla

            return semilla_label, semilla

        elif boton == 'link-etapa4':
            print("se mantiene la semilla")
            return dash.no_update
    else:
        return dash.no_update


# --- > Callback para mezclar a los participantes no ganadores y mostrar el lista de prelación
@app.callback(
    [Output('tabla-orden-prelacion', 'data'), Output('info-orden-prelacion', 'data'),
     Output('sorteo-prelacion-btn', 'children'), Output('sorteo-prelacion-btn', 'disabled'),
     Output('descargar-orden-prelacion-btn', 'children'), Output('descargar-orden-prelacion-btn', 'disabled')],
 
    Input('sorteo-prelacion-btn', 'n_clicks'),

    [State('info-semilla-etapa4', 'data'),
     State('sorteo-boletos', 'data'), State('info-sorteo-terrenos', 'data')],
    
    prevent_initial_call=True
)
def calcularOrdenPrelacion(sorteo_prelacion_btn, info_semilla, sorteo_boletos_data, sorteo_terrenos_data):
    # Se obtiene el DataFrame del sorteo de los numeros
    df_sorteo_numeros = pd.DataFrame.from_dict(sorteo_boletos_data)
    # Se obtiene el dataFrame del sorteo de los lotes
    df_sorteo_lotes = pd.DataFrame.from_dict(sorteo_terrenos_data)

    print("DF DEL SORTEO DE NUMEROS")
    print(df_sorteo_numeros, "\n\n")

    print("DF DEL SORTEO DE LOTES")
    print(df_sorteo_lotes, "\n\n")

    # Se obtiene la lista de números de empleado de todos los participantes
    participantes_total = list(df_sorteo_numeros['num_empleado'])
    # Se obtiene la lista de números de empleado de los participantes ganadores de los lotes
    participantes_ganadores = list(df_sorteo_lotes['num_empleado'])

    # Se obtiene el orden aleatorio de prelación
    df_orden_prelacion = sorteoListaPrelacion(info_semilla, participantes_total, participantes_ganadores)

    return df_orden_prelacion.to_dict('records'), df_orden_prelacion.to_dict('records'), "La lista de prelación ya se ha establecido", True, "Descargar la lista de prelación", False


# Callback para descargar los resultados del lista de prelación
@app.callback(
    [Output('descarga-resultado-orden-prelacion', 'data'), Output('link-resultados-etapa4', 'style')],
    Input('descargar-orden-prelacion-btn', 'n_clicks'),
    State('info-orden-prelacion', 'data'),
    prevent_initial_call=True
)
def descargarResultadoOrdenPrelacion(btn_descarga_resultados, diccionario_resultados_orden_prelacion): 
    texto = "# Lista de prelación de los empleados de confianza que no resultaron ganadores en el\n# \"Sorteo de Trece Lotes del Fraccionamiento Villa Universitaria\"\n\n"
    texto += pd.DataFrame.from_dict(diccionario_resultados_orden_prelacion).to_csv(index=False)
    return dict(content=texto,filename="LISTA_DE_PRELACION.csv"), {}


if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False)


