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