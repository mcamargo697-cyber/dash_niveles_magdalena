import dash
import dash_bootstrap_components as dbc

from src.datos import cargar_datos
from src.figuras import crear_figura_series_tiempo
from src.layout import crear_layout
from src.callbacks import registrar_callbacks


# ============================================================
# 1. Crear app Dash
# ============================================================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True
)

server = app.server


# ============================================================
# 2. Cargar datos y figuras
# ============================================================

df_niveles, df_mannwhitney = cargar_datos()

fig_series_tiempo = crear_figura_series_tiempo(df_niveles)


# ============================================================
# 3. Layout
# ============================================================

app.layout = crear_layout(
    fig_series_tiempo=fig_series_tiempo,
    df_mannwhitney=df_mannwhitney
)


# ============================================================
# 4. Callbacks
# ============================================================

registrar_callbacks(
    app=app,
    fig_series_tiempo=fig_series_tiempo,
    df_mannwhitney=df_mannwhitney
)


# ============================================================
# 5. Ejecutar localmente
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)