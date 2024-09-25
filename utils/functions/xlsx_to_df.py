import pandas as pd


def import_xlsx():
    # Leer el archivo Excel
    df = pd.read_excel('./storage/Peru.xlsx')

    if 'Subnivel 2' in df.columns:
        # Filtrar las columnas que necesitamos del Excel
        df_filtered = df[['Scan FB', 'Scan IG', 'Scan TW', 'Scan YT', 'Scan TK', 'Subnivel 2', 'Subnivel 3', 'Subnivel 4', 'Subnivel 5',
                          'URL Facebook', 'URL Instagram', 'URL Twitter', 'URL YouTube', 'URL TikTok', 'Categoría Facebook', 'Categoria/Criterio', 'Descripción Facebook']]
    else:
        df_filtered = df[['Scan FB', 'Scan IG', 'Scan TW', 'Scan YT', 'Scan TK', 'Subnivel 3', 'Subnivel 4', 'Subnivel 5',
                          'URL Facebook', 'URL Instagram', 'URL Twitter', 'URL YouTube', 'URL TikTok', 'Categoría Facebook', 'Categoria/Criterio', 'Descripción Facebook']]
    del df

    return df_filtered
