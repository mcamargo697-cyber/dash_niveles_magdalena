import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# Estaciones a graficar
# ============================================================

ESTACIONES = {
    "Achi": "Achi",
    "Calamar": "Calamar",
    "El Banco": "ElBanco",
    "Salado Blanco": "SaladoBlanco",
    "Puerto Berrío": "PuertoBerrio",
    "Barrancabermeja": "Barrancabermeja"
}


# ============================================================
# Figura: series de tiempo
# ============================================================

def crear_figura_series_tiempo(df_niveles):
    """
    Crea una figura Plotly con las series temporales de nivel medio diario.
    """

    fig = make_subplots(
        rows=len(ESTACIONES),
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.035,
        subplot_titles=[
            f"Estación {nombre}"
            for nombre in ESTACIONES.keys()
        ]
    )

    for i, (nombre_estacion, columna) in enumerate(ESTACIONES.items(), start=1):

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
        row=len(ESTACIONES),
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

# ============================================================
# Correlación cruzada
# ============================================================

def calcular_correlacion_cruzada(df_niveles, target="Calamar", max_lag=30):
    """
    Calcula la correlación cruzada entre Calamar y las estaciones explicativas.

    lag > 0 significa que la estación explicativa ocurre antes que Calamar.
    """

    explicativas = [
        col for col in ESTACIONES.values()
        if col != target
    ]

    ccf_resultados = {}
    lags_optimos = {}
    corrs_optimas = {}

    for estacion in explicativas:

        resultados = []

        for lag in range(max_lag + 1):
            correlacion = df_niveles[estacion].shift(lag).corr(df_niveles[target])
            resultados.append({
                "lag_dias": lag,
                "correlacion": correlacion
            })

        df_ccf = pd.DataFrame(resultados)

        mejor = df_ccf.loc[df_ccf["correlacion"].idxmax()]

        ccf_resultados[estacion] = df_ccf
        lags_optimos[estacion] = int(mejor["lag_dias"])
        corrs_optimas[estacion] = float(mejor["correlacion"])

    df_lags = pd.DataFrame({
        "Estación": list(lags_optimos.keys()),
        "Lag óptimo [días]": list(lags_optimos.values()),
        "Correlación máxima": list(corrs_optimas.values())
    }).sort_values(
        "Correlación máxima",
        ascending=False
    ).reset_index(drop=True)

    df_lags = df_lags.round({
        "Correlación máxima": 4
    })

    return ccf_resultados, df_lags


def crear_figura_correlacion_cruzada(ccf_resultados, df_lags, target="Calamar"):
    """
    Crea una figura Plotly con las curvas de correlación cruzada.
    """

    fig = make_subplots(
        rows=3,
        cols=2,
        subplot_titles=[
            f"{estacion} vs {target}"
            for estacion in ccf_resultados.keys()
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.10
    )

    posiciones = [
        (1, 1), (1, 2),
        (2, 1), (2, 2),
        (3, 1)
    ]

    for (estacion, df_ccf), (row, col) in zip(ccf_resultados.items(), posiciones):

        lag_optimo = int(
            df_lags.loc[
                df_lags["Estación"] == estacion,
                "Lag óptimo [días]"
            ].iloc[0]
        )

        corr_max = float(
            df_lags.loc[
                df_lags["Estación"] == estacion,
                "Correlación máxima"
            ].iloc[0]
        )

        fig.add_trace(
            go.Scatter(
                x=df_ccf["lag_dias"],
                y=df_ccf["correlacion"],
                mode="lines+markers",
                name=estacion,
                hovertemplate=(
                    "<b>Estación:</b> " + estacion + "<br>" +
                    "<b>Lag:</b> %{x} días<br>" +
                    "<b>Correlación:</b> %{y:.4f}<br>" +
                    "<extra></extra>"
                )
            ),
            row=row,
            col=col
        )

        fig.add_vline(
            x=lag_optimo,
            line_dash="dash",
            annotation_text=f"lag = {lag_optimo} d",
            annotation_position="top",
            row=row,
            col=col
        )

        fig.add_trace(
            go.Scatter(
                x=[lag_optimo],
                y=[corr_max],
                mode="markers",
                marker=dict(size=10),
                name=f"Lag óptimo {estacion}",
                showlegend=False,
                hovertemplate=(
                    "<b>Lag óptimo:</b> " + str(lag_optimo) + " días<br>" +
                    "<b>Correlación máxima:</b> " + f"{corr_max:.4f}" +
                    "<extra></extra>"
                )
            ),
            row=row,
            col=col
        )

        fig.update_xaxes(
            title_text="Lag [días]",
            row=row,
            col=col
        )

        fig.update_yaxes(
            title_text="Correlación",
            row=row,
            col=col
        )

    fig.update_layout(
        title="Correlación cruzada entre Calamar y estaciones explicativas",
        height=1100,
        template="plotly_white",
        showlegend=False,
        hovermode="closest",
        margin=dict(l=70, r=40, t=90, b=60)
    )

    return fig