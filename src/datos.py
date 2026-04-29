from pathlib import Path
import pandas as pd


# ============================================================
# Rutas relativas del proyecto
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

RUTA_NIVELES = DATA_DIR / "Niveles_alineados.csv"
RUTA_MANNWHITNEY = DATA_DIR / "resultados_mannwhitney.csv"


# ============================================================
# Cargar datos
# ============================================================

def cargar_datos():
    """
    Carga los datos necesarios para el dashboard.
    """

    df_niveles = pd.read_csv(RUTA_NIVELES)
    df_mannwhitney = pd.read_csv(RUTA_MANNWHITNEY)

    df_niveles["Fecha"] = pd.to_datetime(
        df_niveles["Fecha"],
        errors="coerce"
    )

    df_niveles = df_niveles.sort_values("Fecha")

    return df_niveles, df_mannwhitney