import dash_core_components as dcc
import dash
import dash_html_components as html
import pandas as pd
import os
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib as plt
import matplotlib.pyplot as plt
import altair as alt
from vega_datasets import data
from matplotlib import cm
from math import log10
import matplotlib.ticker as mtick
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#app = dash.Dash(__name__)

CONTEO_DE_PROCESOS = pd.read_csv('CONTEO_DE_PROCESOS.csv', 
                 sep = ',', parse_dates= True,
                        thousands=',', decimal='.',
                 dtype={
                     'Nit Entidad': str
                 })


CONTEO_DE_PROCESOS1 = CONTEO_DE_PROCESOS[CONTEO_DE_PROCESOS.DEPARTAMENTO.isin(["Guainía","Vaupés","Vichada","Chocó","Sucre","Magdalena"])]
CONTEO_DE_PROCESOS2 = CONTEO_DE_PROCESOS1[CONTEO_DE_PROCESOS1.GRUPO_DELITO.isin(["DESAPARICION FORZADA","TRATA DE PERSONAS"])]

fig_aleja1 = px.treemap(CONTEO_DE_PROCESOS2, path=['ESTADO_NOTICIA','GRUPO_DELITO', 'DEPARTAMENTO'], 
                 values='TOTAL_PROCESOS', 
                 color='GRUPO_DELITO',
                 title='Estado del proceso ')


fig_esta = px.pie(CONTEO_DE_PROCESOS2, values='TOTAL_PROCESOS', names='GRUPO_DELITO',
             title='Porcentaje grupo de delito ',color_discrete_sequence=px.colors.sequential.Sunset)


available_departamentos = CONTEO_DE_PROCESOS2['DEPARTAMENTO'].unique()
available_municipios = CONTEO_DE_PROCESOS2["MUNICIPIO"].unique()
available_filtro_general = CONTEO_DE_PROCESOS2["GRUPO_DELITO"].unique()
#Municipio_filter = CONTEO_DE_PROCESOS2['DEPARTAMENTO'].unique()
#Municipio_filter_2 = CONTEO_DE_PROCESOS2['MUNICIPIO'].unique()
condena_filtro = CONTEO_DE_PROCESOS2["CONDENA"].unique()
captura_filtro = CONTEO_DE_PROCESOS2["CAPTURA"].unique()



app.layout = html.Div(
    children=[
        html.H1(children="PROYECTO VISUALIZACIÓN",
            style = {
                        'textAlign': 'center',
            }),
        html.H2(children="Introducción"),
        html.P(
            children='''
                En el presente trabajo se platea la realización de distintas visualizaciones donde se evidencie el comportamiento 
                temporal, descripción y clasificación de dos grupos de delitos, los cuales son significativos para los departamentos 
                de selección, adicionalmente, son delitos de los cuales en un país como Colombia se han venido reflejados en el 
                transcurso de la historia, estos delitos hacen referencia a trata de personas y desaparición forzada, adicional a lo 
                anterior se lleva a cabo un filtro el cual va  a depender el resto de las visualizaciones con el objetivo de evidenciar  
                que tanto cambia los resultados de un departamento y/o municipio con estos delitos en particular,  conjuntamente el 
                porqué de esta aplicación es identificar los eventos más relevantes que se pudieron evidenciar en análisis de entregas  
                anteriores.

                
                En esta aplicación se seleccionó seis departamentos los cuales corresponden a Guainía, Vaupés, Vichada, Chocó, Sucre, 
                Magdalena, los cuales son los departamentos con mayor desigualdad y pobreza según fuentes externas, el porqué de estos 
                departamentos está relacionado con la relación que hay entre falta de posibilidades, corrupción y pobreza monetaria con 
                respecto al incremento de delito. Para finalizar la aplicación quiere manifestar los 6 departamentos más pobres como se 
                comportaron los delitos trata de personas y desaparición forzada, a través del tiempo, si su mayoría de casos estaban 
                activos o inactivos y si hubo captura y condena. Todo esto se hizo con el fin de tener un análisis más detallado de 
                estos departamentos.

            '''),
        html.H2(children="ETL"),
        html.P(
            children='''
                La base fue obtenida por medio de la siguiente referencia 
                [Datos abiertos justicia y derecho conteos de procesos](https://www.datos.gov.co/Justicia-y-Derecho/Conteo-de-Procesos/q6re-36rh), 
                en la cual se puede evidenciar la tabla de contenido, del significado de cada una de las diferentes variables. Se cuenta con una 
                base inicial, la cual tiene  2062369 registros con 22 diferentes variables, para el proceso de ETL se realizó una limpieza de valores  
                inconsistentes  en diferentes periodos del tiempo, esta limpieza se realizó por medio de depuración de valores, dado que su cantidad 
                era mínima, adicionalmente se realizó una transformación de signos de puntuación los cuales permitían que sus resultados no fueran reales,
                conjuntamente a lo anterior se depuraron valores faltantes los cuales no superaban el 0.72% de la cantidad de registros, pero si se 
                eliminó la variable atipicidad inexistencia dado que no era fundamental para el estudio de investigación propuesto. Por último se 
                trabajó con la base la cual cuenta con   $2047396 registros 21 características. 
            '''),

        html.Div(children='''
                 DELITO
                 '''),

        dcc.Dropdown(
                    id='Filtro_General',
                    options=[{'label': i, 'value': i} for i in available_filtro_general],
                    value='DESAPARICION FORZADA'
                    ),
        html.Div(children='''
                 DEPARTAMENTO
                 '''),
        dcc.Dropdown(
                    id='grafico_dep_1',
                    options=[{'label': i, 'value': i} for i in available_departamentos],
                    value='Guainía',
                    clearable=False
                    ),
        html.Div(children='''
                 MUNICIPIO
                 '''),
        dcc.Dropdown(
                    id='grafico_mun_1',
                    options=[{'label': i, 'value': i} for i in available_municipios],
                    value='BARRANCO MINAS', 
                    clearable=False
                    ),
#          dcc.Dropdown(
#        id='values', 
#        value='Guainía', 
#        options=[{'value': x, 'label': x} 
#                 for x in available_departamentos],
#        clearable=False
#    ),
#    dcc.Dropdown(
#        id='Captura', 
#        value='BARRANCO MINAS', 
#        options=[{'value': x, 'label': x} 
#                 for x in available_municipios],
#        clearable=False
#    ),
        html.Div([
            html.Div([
                html.H1(children="Visualización Temporal por Departamento: Gabriela Cortés"),
                html.Div(children='''
                    En esta visualización el usuario puede observar el comportamiento temporal
                    que tipo el grupo de delito seleccionado a inicio de la visualización por 
                    departamento de interés, Adicionalmente esta visualización tiene como objetivo 
                    ayudar a que el usuario descubra como se comportó el departamento con uno de los 
                    delitos más graves que hay en el país y así poder compararlo con los otros seis 
                    departamentos que más se encuentran en vulnerabilidad.  
                    '''),


                dcc.Graph(
                    id='gafico_1_g'
                    ),
                ], className='six columns'),
            ], className='row'),

        html.Div([
            html.Div([
                html.H1(children="Visualización Temporal por Municipio: Gabriela Cortés"),
                html.Div(children='''
                    La presente visualización tiene como objetivo permitir que el usuario 
                    puede observar el comportamiento temporal según su  grupo de delito 
                    seleccionado a inicio de la visualización por municipio de interés, 
                    adicionalmente esta visualización ayuda a que el usuario descubra 
                    como se comportó el municipio con uno de los delitos más graves que 
                    hay en el país y así poder compararlo con los otros municipios del 
                    país que pertenezcan a los departamentos  que más se encuentran en vulnerabilidad, 
                    adicionalmente se recomienda al usuario que para un conocimiento más amplio selecciones 
                    los municipios que pertenezcan al departamento de la primera visualización.  
                    '''),

                dcc.Graph(
                    id='gafico_2_g'
                    ),
                ], className='six columns'),

            ], className='row'),
        html.Div([
        html.Div([
            html.H1(children='Estado del proceso: M.Alejandra Bolivar'),#
            html.Div(children='''
                Que: Basados en el Framework de Tamara, evidenciamos que el Dataset cuenta con atributos categóricos 
                para casi todas las variables excepto total de procesos y departamento. Total de procesos son variables ordenadas 
                cuantitativas y cuenta con una dirección secuencial, el tipo de Data Set utilizado será un Treemap que contienen 
                clasificaciones, son datos estáticos, es decir, que no cambian en el tiempo. Tiene 1 atributo cuantitativo en los nodos de las hojas.

                Porque: En el caso de los verbos utilizados para la descripción de la visualización, se utilizaron el descubrir, y analizar por medio del Treemaps el análisis
                básico de las proporciones de los valores que tiene el estado de la noticia y los dos delitos escogidos, además se buscara la segmentación de estos procesos basados en los departamentos más pobres de Colombia. 
                En el caso de los sustantivos que se utilizaron para las variables se tienen en cuenta la relación y proporción. Adicionalmente, la visualización tiene estructura jerárquica donde les asigna un tamaño y un orden en función de la variable cuantitativa. 

                Como: Lo que se quiere es saber de qué manera fue hecha la visualización, fueron estructurados en forma de árbol, por jerarquía, como un conjunto de rectángulos anidados. A cada grupo se le asigna un rectángulo, que después
                 se combina con rectángulos más pequeños que representan subgrupos. El tamaño y el color se usan para mostrar dimensiones numéricas independientes de los datos.

                En esta visualización el usuario puede ver el estado de noticia con más procesos, y cual de los 
                delitos escogidos es el más frecuentes en los departamentos más pobres de Colombia. 
            '''),#
            dcc.Graph(
                id='example-graph-2',
                figure=fig_aleja1
            ),  
        ], className='six columns'),

        html.Div([
            html.H2(children='Porcentaje de inactivos: M.Alejandra Bolivar'),#
            html.Div(children='''
            	Como se pudo ver en la grafica anterior el estado inactivo es el que más procesos tiene por lo cual se hara un filtro para 
            	este estado y se mirara el porcentaje que tiene cada uno de los delitos en este estado. El usuario puede ver el porcentaje para el estado inactivo que es 
                el que más procesos tiene de acuerdo a su grupo de delito. 

                Que: Basados en el Framework de Tamara, para esta primera visualización lo que se quiere representar 
                es el estado de la noticia criminal al momento de la consulta del dato en el sistema de información, 
                se encuentra evidenciado con un Dataset de tabla que contiene atributos categóricos, y luego explicado en porcentaje.

                Porque: Se quiere mirar el comportamiento y la proporción que tiene el estado de la noticia, donde se descubre y se
                analiza que tantos procesos están siendo revisados y que tantos no. Además, se identifican ciertas características y se pueden comparar con más cosas más adelantes.
                Está definida por la forma.

                Como: La visualización cuenta con una gráfica sencilla que compara dos categorías activo e inactivo, se hace por medio de un gráfico de torta,
                 se dan sus respectivos porcentajes y utiliza el canal de color.

                
            '''),#
            dcc.Graph(
                id='example_estado',
                figure=fig_esta
            ),  
        ], className='six columns'),
    html.H2(children="Comparación: M.Alejandra Bolivar"),
    html.Div(children='''
            Ya teniendo en cuenta el porcentaje de cada uno de los delitos el usuario puede hacer una comparación entre el departamento y su 
            municipio. 

            Que: En esta visualización lo que se quiere representar es de los dos delitos escogidos que municipios cuentan con más procesos de este tipo
            se encuentra evidenciado con un Dataset de tabla que contiene atributos categóricos.

            Porque: Se quiere presentar cuantos datos existen por Grupo de delito, por departamento y por municipio, se utilizara el search,
             con el cual se identificara y se harán comparaciones.

            Como: La visualización cuenta con una gráfica estática pero que contiene dos filtros uno para el departamento y uno para el municipio 
            que compara los procesos y se hace por medio de un gráfico de barras.

            En estas visualizaciones el usuario puede hacer por medio dos filtros una 
                comparación entre el departamento y el municipio basado en el grupo de delito, esto
                 con el fin de que saber cómo se comportaron los delitos deaparición forzada y trata de personas
                en los departamentos más pobres de Colombia, 
                el usuario puede escoger el municipio y el departamento que desee para poder hacer la comparación
                entre estos.
            '''),

    dcc.Graph(
        id="pie-chart"
        ),
    dcc.Graph(
            id='Grafico_municipio'
            )
        ], className='row'),
 #########################################################3
 ###########################################################
 ###############################################################
 ###########################################################################
 ########################################################################################
    html.Div([
        html.H1(children = "Visualizaciones Juan Sarmiento"),
        html.Div(children = ''' 
                En las siguientes visualizaciones se busca mostrar la cantidad de procesos que no han tenido ni captura ni condena para el delito seleccionado en el municipio seleccionado.
            '''),
        dcc.Graph(
            id='gafico_1_j'
            ),
        dcc.Graph(
            id='gafico_2_j'
            )
        ], className='row'),

])

#####################################################################################3
##########################################################################################
#############################################################################################
#############################################################################################


@app.callback(
    dash.dependencies.Output('gafico_1_g','figure'),
    [dash.dependencies.Input('grafico_dep_1','value'),
    dash.dependencies.Input('Filtro_General','value')]
    )
def update_graph(departamento_value,crimen_value):
    CONTEO_DE_PROCESOS_G=CONTEO_DE_PROCESOS2[CONTEO_DE_PROCESOS2["DEPARTAMENTO"] == departamento_value]
    CONTEO_DE_PROCESOS_G2=CONTEO_DE_PROCESOS_G[CONTEO_DE_PROCESOS_G["GRUPO_DELITO"] == crimen_value]

    fig_d_g = px.bar(CONTEO_DE_PROCESOS_G2, x="ANIO_HECHO", y="TOTAL_PROCESOS", title='Comportamiento Temporal por Departamento',
     category_orders = {"ANIO_HECHO":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]})

    return fig_d_g



# Viz2
@app.callback(
    dash.dependencies.Output('gafico_2_g','figure'),
    [dash.dependencies.Input('grafico_mun_1','value'),
    dash.dependencies.Input('Filtro_General','value')]
    )
def update_graph(munucipio_value,crimen1_value):
    
    CONTEO_DE_PROCESOS_G3=CONTEO_DE_PROCESOS2[CONTEO_DE_PROCESOS2["MUNICIPIO"] == munucipio_value]
    CONTEO_DE_PROCESOS_G4=CONTEO_DE_PROCESOS_G3[CONTEO_DE_PROCESOS_G3["GRUPO_DELITO"] == crimen1_value]


    fig_d_g2 = px.bar(CONTEO_DE_PROCESOS_G4, x="ANIO_HECHO", y="TOTAL_PROCESOS", title='Comportamiento Temporal por Municipio', 
        category_orders = {"ANIO_HECHO":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]})

    return fig_d_g2

@app.callback(
    dash.dependencies.Output("pie-chart", "figure"), 
    [dash.dependencies.Input("grafico_dep_1", "value"),
    dash.dependencies.Input('grafico_mun_1', 'value')])

def update_graph( Municipio_filter,Municipio_filter_2):

    
    CONTEO_DE_PROCESOS1 = CONTEO_DE_PROCESOS[CONTEO_DE_PROCESOS.DEPARTAMENTO.isin(["Guainía","Vaupés","Vichada","Chocó","Sucre","Magdalena"])]
    CONTEO_DE_PROCESOS_12 = CONTEO_DE_PROCESOS1[CONTEO_DE_PROCESOS1.GRUPO_DELITO.isin(['DESAPARICION FORZADA','TRATA DE PERSONAS'])]
    CONTEO_DE_incativos = CONTEO_DE_PROCESOS_12[CONTEO_DE_PROCESOS_12.ESTADO_NOTICIA.isin(["INACTIVO"])]


    CONTEO_DE_PROCESOS_3 = CONTEO_DE_incativos[CONTEO_DE_incativos['DEPARTAMENTO'] == Municipio_filter]
    
    

    fig = px.bar(CONTEO_DE_PROCESOS_3, x="GRUPO_DELITO", y="TOTAL_PROCESOS", color="DEPARTAMENTO", title="Grafico Departamento")
    return fig



@app.callback(
    dash.dependencies.Output("Grafico_municipio", "figure"), 
    [dash.dependencies.Input("grafico_dep_1", "value"),
    dash.dependencies.Input('grafico_mun_1', 'value')])

def update_graph(Municipio_select, Municipio_filter_2):


    CONTEO_DE_incativos = CONTEO_DE_PROCESOS1[CONTEO_DE_PROCESOS1.ESTADO_NOTICIA.isin(["INACTIVO"])]
    CONTEO_DE_PROCESOS_2 = CONTEO_DE_incativos[CONTEO_DE_incativos.GRUPO_DELITO.isin(["DESAPARICION FORZADA","TRATA DE PERSONAS"])]

    CONTEO_DE_PROCESOS3 = CONTEO_DE_PROCESOS_2[CONTEO_DE_PROCESOS_2['MUNICIPIO'] == Municipio_filter_2]

    

    fig_bar = px.bar(CONTEO_DE_PROCESOS3, x="GRUPO_DELITO", y="TOTAL_PROCESOS", color="MUNICIPIO", title="Grafico Municipio")
    return fig_bar


@app.callback(
    dash.dependencies.Output('gafico_1_j','figure'),
    [dash.dependencies.Input('grafico_dep_1','value'),
    dash.dependencies.Input('Filtro_General','value')]
    )
def update_graph(departamento_value,crimen_value):
    CONTEO_DE_PROCESOS_G=CONTEO_DE_PROCESOS2[CONTEO_DE_PROCESOS2["DEPARTAMENTO"] == departamento_value]
    CONTEO_DE_PROCESOS_G2=CONTEO_DE_PROCESOS_G[CONTEO_DE_PROCESOS_G["GRUPO_DELITO"] == crimen_value]
   # CONTEO_DE_PROCESOS_G2=CONTEO_DE_PROCESOS_G2[CONTEO_DE_PROCESOS_G2["CAPTURA"] == capture]

    fig_d_g = px.bar(CONTEO_DE_PROCESOS_G2, x="ANIO_HECHO", y="TOTAL_PROCESOS",  color="CAPTURA",
     category_orders = {"ANIO_HECHO":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]})

    return fig_d_g

@app.callback(
    dash.dependencies.Output('gafico_2_j','figure'),
    [dash.dependencies.Input('grafico_dep_1','value'),
    dash.dependencies.Input('Filtro_General','value')]
    )
def update_graph(departamento_value,crimen_value):
    CONTEO_DE_PROCESOS_G=CONTEO_DE_PROCESOS2[CONTEO_DE_PROCESOS2["DEPARTAMENTO"] == departamento_value]
    CONTEO_DE_PROCESOS_G2=CONTEO_DE_PROCESOS_G[CONTEO_DE_PROCESOS_G["GRUPO_DELITO"] == crimen_value]
   # CONTEO_DE_PROCESOS_G2=CONTEO_DE_PROCESOS_G2[CONTEO_DE_PROCESOS_G2["CONDENA"] == condena]

    fig_d_g = px.bar(CONTEO_DE_PROCESOS_G2, x="ANIO_HECHO", y="TOTAL_PROCESOS",  color="CONDENA", 
     category_orders = {"ANIO_HECHO":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]})

    return fig_d_g



if __name__ == "__main__":
    app.run_server(debug=True)



