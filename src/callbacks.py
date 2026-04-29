import dash
from dash import Input, Output

from src.secciones import (
    crear_seccion_exploracion_inicial,
    crear_seccion_imputacion,
    crear_seccion_correlacion_cruzada,
    crear_seccion_estructura_temporal
)


# ============================================================
# Registrar callbacks
# ============================================================

def registrar_callbacks(app, fig_series_tiempo, df_mannwhitney):

    @app.callback(
        Output("contenido-eda", "children"),
        Input("btn-correlacion-cruzada", "n_clicks"),
        Input("btn-exploracion-inicial", "n_clicks"),
        Input("btn-estructura-temporal", "n_clicks"),
        Input("btn-imputacion-datos", "n_clicks")
    )
    def actualizar_contenido_eda(
        n_correlacion,
        n_exploracion,
        n_estructura,
        n_imputacion
    ):

        ctx = dash.callback_context

        if not ctx.triggered:
            return crear_seccion_exploracion_inicial(fig_series_tiempo)

        boton_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if boton_id == "btn-correlacion-cruzada":
            return crear_seccion_correlacion_cruzada()

        elif boton_id == "btn-exploracion-inicial":
            return crear_seccion_exploracion_inicial(fig_series_tiempo)

        elif boton_id == "btn-estructura-temporal":
            return crear_seccion_estructura_temporal()

        elif boton_id == "btn-imputacion-datos":
            return crear_seccion_imputacion(df_mannwhitney)

        return crear_seccion_exploracion_inicial(fig_series_tiempo)