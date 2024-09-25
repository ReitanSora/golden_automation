import pandas as pd


def export_xlsx(updated, failed):

    # Convertir los arrays a DataFrames
    df_updated = pd.DataFrame(updated)
    df_failed = pd.DataFrame(failed)

    # Guardar los DataFrames en archivos Excel con información detallada antes y después de la ejecución
    df_updated.to_excel(
        './storage/logs/registros_actualizados.xlsx', index=False)
    df_failed.to_excel('./storage/logs/registros_fallidos.xlsx', index=False)
