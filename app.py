import dash
import dash_bootstrap_components as dbc

from src.datos import cargar_datos
from src.figuras import (
    crear_figura_series_tiempo,
    calcular_correlacion_cruzada,
    crear_figura_correlacion_cruzada
)

from src.layout import crear_layout
from src.callbacks import registrar_callbacks

# 1. Crear app Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True
)

server = app.server



# 2. Cargar datos y figuras
df_niveles, df_mannwhitney = cargar_datos()

fig_series_tiempo = crear_figura_series_tiempo(df_niveles)

ccf_resultados, df_lags = calcular_correlacion_cruzada(
    df_niveles=df_niveles,
    target="Calamar",
    max_lag=30
)

fig_correlacion_cruzada = crear_figura_correlacion_cruzada(
    ccf_resultados=ccf_resultados,
    df_lags=df_lags,
    target="Calamar"
)

# 3. Layout
app.layout = crear_layout(
    fig_series_tiempo=fig_series_tiempo,
    df_mannwhitney=df_mannwhitney,
    fig_correlacion_cruzada=fig_correlacion_cruzada,
    df_lags=df_lags
)


registrar_callbacks(
    app=app,
    fig_series_tiempo=fig_series_tiempo,
    df_mannwhitney=df_mannwhitney,
    fig_correlacion_cruzada=fig_correlacion_cruzada,
    df_lags=df_lags
)


# ============================================================
# Ejecutar localmente o dentro de Docker
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=9000
    )