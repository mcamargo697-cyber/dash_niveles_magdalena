from dash import html
import dash_bootstrap_components as dbc

from src.secciones import (
    crear_seccion_exploracion_inicial,
    crear_seccion_imputacion,
    crear_seccion_correlacion_cruzada,
    crear_seccion_estructura_temporal
)


# ============================================================
# Crear layout principal
# ============================================================

def crear_layout(fig_series_tiempo, df_mannwhitney):

    seccion_exploracion_inicial = crear_seccion_exploracion_inicial(fig_series_tiempo)

    return dbc.Container([

        # ====================================================
        # Encabezado
        # ====================================================

        dbc.Row([
            dbc.Col([

                html.H1(
                    "Dashboard de niveles del río Magdalena",
                    className="text-center mt-4 mb-2"
                ),

                html.P(
                    "Segunda entrega del proyecto de Machine Learning: análisis exploratorio, "
                    "validación estadística de la imputación y visualización de resultados.",
                    className="text-center text-muted mb-4",
                    style={"fontSize": "17px"}
                )

            ])
        ]),

        # ====================================================
        # Pestañas principales
        # ====================================================

        dbc.Tabs([

            # ------------------------------------------------
            # Pestaña 1: Introducción
            # ------------------------------------------------

            dbc.Tab(label="Introducción", children=[

                dbc.Card([
                    dbc.CardBody([

                        html.H3("Introducción", className="card-title"),

                        html.P(
                            "Este dashboard presenta el análisis de series temporales de nivel medio diario "
                            "en estaciones hidrológicas asociadas al río Magdalena. La aplicación permite "
                            "explorar visualmente los datos, evaluar el efecto de la imputación y organizar "
                            "los resultados de la segunda entrega del proyecto de Machine Learning.",
                            className="card-text"
                        ),

                        html.P(
                            "El tablero está organizado en tres secciones principales: Introducción, EDA y Modelos. "
                            "La sección EDA contiene los análisis exploratorios, las gráficas interactivas y los "
                            "resultados del test Mann–Whitney U. La sección Modelos queda preparada para incluir "
                            "posteriormente los resultados de los modelos predictivos.",
                            className="card-text"
                        ),

                        dbc.Row([

                            dbc.Col(
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H4("6", className="card-title text-center"),
                                        html.P("Estaciones analizadas", className="text-center text-muted")
                                    ])
                                ], color="light", outline=True),
                                md=4
                            ),

                            dbc.Col(
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H4("Mann–Whitney U", className="card-title text-center"),
                                        html.P("Validación estadística", className="text-center text-muted")
                                    ])
                                ], color="light", outline=True),
                                md=4
                            ),

                            dbc.Col(
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H4("Plotly", className="card-title text-center"),
                                        html.P("Gráficas interactivas con zoom", className="text-center text-muted")
                                    ])
                                ], color="light", outline=True),
                                md=4
                            ),

                        ], className="mt-4")

                    ])
                ], className="mt-4 mb-4 shadow-sm")

            ]),

            # ------------------------------------------------
            # Pestaña 2: EDA
            # ------------------------------------------------

            dbc.Tab(label="EDA", children=[

                dbc.Card([
                    dbc.CardBody([

                        html.H3("Análisis exploratorio de datos", className="card-title"),

                        html.P(
                            "Seleccione una de las opciones para visualizar los análisis exploratorios "
                            "desarrollados en la segunda entrega.",
                            className="card-text"
                        ),

                        dbc.Row([

                            dbc.Col(
                                dbc.Button(
                                    "Correlación Cruzada",
                                    id="btn-correlacion-cruzada",
                                    color="primary",
                                    outline=True,
                                    className="w-100 mb-2"
                                ),
                                md=3
                            ),

                            dbc.Col(
                                dbc.Button(
                                    "Exploración Inicial de datos",
                                    id="btn-exploracion-inicial",
                                    color="primary",
                                    outline=True,
                                    className="w-100 mb-2"
                                ),
                                md=3
                            ),

                            dbc.Col(
                                dbc.Button(
                                    "Estructura temporal",
                                    id="btn-estructura-temporal",
                                    color="primary",
                                    outline=True,
                                    className="w-100 mb-2"
                                ),
                                md=3
                            ),

                            dbc.Col(
                                dbc.Button(
                                    "Imputación de datos",
                                    id="btn-imputacion-datos",
                                    color="primary",
                                    outline=True,
                                    className="w-100 mb-2"
                                ),
                                md=3
                            ),

                        ], className="mt-3"),

                    ])
                ], className="mt-4 mb-4 shadow-sm"),

                html.Div(
                    id="contenido-eda",
                    children=seccion_exploracion_inicial
                )

            ]),

            # ------------------------------------------------
            # Pestaña 3: Modelos
            # ------------------------------------------------

            dbc.Tab(label="Modelos", children=[

                dbc.Card([
                    dbc.CardBody([

                        html.H3("Modelos de Machine Learning", className="card-title"),

                        html.P(
                            "Esta sección está destinada a presentar los modelos desarrollados durante "
                            "la segunda entrega del proyecto. Aquí se pueden incluir posteriormente las "
                            "métricas de desempeño, comparación entre modelos, predicciones y análisis "
                            "de errores.",
                            className="card-text"
                        ),

                        dbc.Alert(
                            "Sección preparada para incluir resultados de modelos como SVR, Ridge u otros "
                            "modelos evaluados en el proyecto.",
                            color="info"
                        )

                    ])
                ], className="mt-4 mb-4 shadow-sm")

            ])

        ])

    ], fluid=True)