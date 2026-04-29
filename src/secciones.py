from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc


# ============================================================
# Sección: Exploración inicial
# ============================================================

def crear_seccion_exploracion_inicial(fig_series_tiempo):

    return dbc.Card([
        dbc.CardBody([

            html.H3("Exploración inicial de datos", className="card-title"),

            html.P(
                "En esta sección se presentan las series temporales de nivel medio diario "
                "para las estaciones seleccionadas. Las gráficas fueron elaboradas con Plotly, "
                "por lo que permiten hacer zoom, desplazamiento horizontal, inspección de valores "
                "y descarga como imagen.",
                className="card-text"
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
            )

        ])
    ], className="mt-4 mb-4 shadow-sm")


# ============================================================
# Sección: Imputación de datos
# ============================================================

def crear_seccion_imputacion(df_mannwhitney):

    return dbc.Card([
        dbc.CardBody([

            html.H3("Imputación de datos", className="card-title"),

            html.P(
                "La prueba Mann–Whitney U se aplicó para comparar la serie original no imputada "
                "con la serie imputada. El objetivo fue evaluar si la imputación generó diferencias "
                "estadísticamente significativas en la distribución de los datos.",
                className="card-text"
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
                className="text-muted",
                style={"fontSize": "13px"}
            )

        ])
    ], className="mt-4 mb-4 shadow-sm")


# ============================================================
# Sección: Correlación cruzada
# ============================================================

def crear_seccion_correlacion_cruzada():

    return dbc.Card([
        dbc.CardBody([

            html.H3("Correlación cruzada", className="card-title"),

            dbc.Alert(
                "Esta sección queda preparada para incluir las gráficas y resultados "
                "de correlación cruzada entre estaciones.",
                color="secondary"
            )

        ])
    ], className="mt-4 mb-4 shadow-sm")


# ============================================================
# Sección: Estructura temporal
# ============================================================

def crear_seccion_estructura_temporal():

    return dbc.Card([
        dbc.CardBody([

            html.H3("Estructura temporal", className="card-title"),

            dbc.Alert(
                "Esta sección queda preparada para incluir el análisis de estructura temporal "
                "de las series, como tendencia, estacionalidad, rezagos o patrones anuales.",
                color="secondary"
            )

        ])
    ], className="mt-4 mb-4 shadow-sm")