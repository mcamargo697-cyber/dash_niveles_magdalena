import os
from pathlib import Path

import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots



# 1. Crear app Dash
external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/litera/bootstrap.min.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Importante para Render
server = app.server


# 2. Rutas relativas
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

RUTA_NIVELES = DATA_DIR / "Niveles_alineados.csv"
RUTA_MANNWHITNEY = DATA_DIR / "resultados_mannwhitney.csv"


# 3. Cargar datos
df_niveles = pd.read_csv(RUTA_NIVELES)
df_mannwhitney = pd.read_csv(RUTA_MANNWHITNEY)

df_niveles["Fecha"] = pd.to_datetime(
    df_niveles["Fecha"],
    errors="coerce"
)

df_niveles = df_niveles.sort_values("Fecha")



# 4. Estaciones a graficar
estaciones = {
    "Achi": "Achi",
    "Calamar": "Calamar",
    "El Banco": "ElBanco",
    "Salado Blanco": "SaladoBlanco",
    "Puerto Berrío": "PuertoBerrio",
    "Barrancabermeja": "Barrancabermeja"
}



# 5. Función para crear gráfica Plotly
def crear_figura_series_tiempo():

    fig = make_subplots(
        rows=len(estaciones),
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.035,
        subplot_titles=[
            f"Estación {nombre}"
            for nombre in estaciones.keys()
        ]
    )

    for i, (nombre_estacion, columna) in enumerate(estaciones.items(), start=1):

        fig.add_trace(
            go.Scatter(
                x=df_niveles["Fecha"],
                y=df_niveles[columna],
                mode="lines",
                name=nombre_estacion,
                line=dict(width=1),
                hovertemplate=(
                    "<b>Estación:</b> " + nombre_estacion + "<br>" +
                    "<b>Fecha:</b> %{x|%Y-%m-%d}<br>" +
                    "<b>Nivel:</b> %{y:.2f} cm<br>" +
                    "<extra></extra>"
                )
            ),
            row=i,
            col=1
        )

        fig.update_yaxes(
            title_text="Nivel [cm]",
            showgrid=True,
            row=i,
            col=1
        )

    fig.update_xaxes(
        title_text="Fecha",
        showgrid=True,
        row=len(estaciones),
        col=1
    )

    fig.update_layout(
        title="Series temporales de nivel medio diario",
        height=1400,
        template="plotly_white",
        hovermode="x unified",
        showlegend=False,
        margin=dict(l=70, r=40, t=90, b=60)
    )

    return fig


fig_series_tiempo = crear_figura_series_tiempo()



# 6. Layout
app.layout = html.Div([

    html.Div([

        html.H1(
            "Dashboard de niveles del río Magdalena",
            style={
                "textAlign": "center",
                "marginTop": "25px",
                "marginBottom": "10px"
            }
        ),

        html.P(
            "Visualización interactiva de series de nivel medio diario y "
            "resultados del test Mann–Whitney U para evaluar el efecto de la imputación.",
            style={
                "textAlign": "center",
                "fontSize": "17px",
                "marginBottom": "35px"
            }
        ),

    ], className="container"),


    html.Div([

        html.H3("1. Series temporales de nivel medio diario"),

        html.P(
            "Las siguientes gráficas fueron generadas con Plotly. "
            "Permiten hacer zoom, desplazarse horizontalmente, inspeccionar valores "
            "y descargar la figura como imagen."
        ),

        dcc.Graph(
            figure=fig_series_tiempo,
            config={
                "displayModeBar": True,
                "scrollZoom": True,
                "displaylogo": False,
                "toImageButtonOptions": {
                    "format": "png",
                    "filename": "series_tiempo_nivel",
                    "height": 1400,
                    "width": 1200,
                    "scale": 2
                }
            }
        ),

    ], className="container", style={"marginBottom": "45px"}),


    html.Div([

        html.H3("2. Resultados del test Mann–Whitney U"),

        html.P(
            "Comparación entre la serie original no imputada y la serie imputada "
            "para evaluar si existen diferencias estadísticamente significativas."
        ),

        dash_table.DataTable(
            data=df_mannwhitney.to_dict("records"),
            columns=[
                {"name": col, "id": col}
                for col in df_mannwhitney.columns
            ],
            page_size=10,

            style_table={
                "overflowX": "auto",
                "marginTop": "15px",
                "marginBottom": "25px"
            },

            style_cell={
                "textAlign": "center",
                "padding": "8px",
                "fontFamily": "Arial",
                "fontSize": "14px",
                "whiteSpace": "normal",
                "height": "auto",
                "minWidth": "110px",
                "maxWidth": "180px"
            },

            style_header={
                "fontWeight": "bold",
                "backgroundColor": "#f2f2f2",
                "border": "1px solid #d9d9d9"
            },

            style_data={
                "border": "1px solid #e6e6e6"
            },

            style_data_conditional=[
                {
                    "if": {
                        "filter_query": '{¿Diferencia significativa?} = "Sí"'
                    },
                    "backgroundColor": "#ffe6e6",
                    "fontWeight": "bold"
                },
                {
                    "if": {
                        "filter_query": '{¿Diferencia significativa?} = "No"'
                    },
                    "backgroundColor": "#e6f4ea"
                }
            ]
        ),

        html.P(
            "Nota: Se considera diferencia estadísticamente significativa cuando "
            "el p-valor es menor que 0.05.",
            style={
                "fontSize": "13px",
                "color": "#555",
                "marginTop": "8px"
            }
        )

    ], className="container", style={"marginBottom": "45px"}),

])


# 7. Ejecutar localmente
if __name__ == "__main__":
    app.run(debug=True)