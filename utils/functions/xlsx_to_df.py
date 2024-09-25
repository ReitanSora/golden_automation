import pandas as pd
from decouple import config

def import_xlsx():
    # Leer el archivo Excel
    df = pd.read_excel(f'./storage/{config('FILE_NAME') if config('FILE_NAME') != None else 'Peru.xlsx'}')

    if config('EXCEL_SUBZONE_2') in df.columns:
        # Filtrar las columnas que necesitamos del Excel
        df_filtered = df[['Fecha', 'Scan FB', 'Scan IG', 'Scan TW', 'Scan YT', 'Scan TK', config('EXCEL_SUBZONE_2'), config('EXCEL_SUBZONE_3'), config('EXCEL_SUBZONE_4'), config('EXCEL_SUBZONE_5'),
                          'URL Facebook', 'URL Instagram', 'URL Twitter', 'URL YouTube', 'URL TikTok', 'Categoría Facebook', 'Categoria/Criterio', 'Descripción Facebook']]
    else:
        df_filtered = df[['Fecha', 'Scan FB', 'Scan IG', 'Scan TW', 'Scan YT', 'Scan TK', config('EXCEL_SUBZONE_3'), config('EXCEL_SUBZONE_4'), config('EXCEL_SUBZONE_5'),
                          'URL Facebook', 'URL Instagram', 'URL Twitter', 'URL YouTube', 'URL TikTok', 'Categoría Facebook', 'Categoria/Criterio', 'Descripción Facebook']]
    del df

    return df_filtered
