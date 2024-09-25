import pandas as pd
import unicodedata
import re


# Función para eliminar tildes y normalizar cadenas
def normalize(text):
    if not pd.isna(text):  # Verificamos si el texto es válido
        # Eliminar tildes
        text = unicodedata.normalize('NFD', text).encode(
            'ascii', 'ignore').decode('utf-8')
        # Eliminar espacios innecesarios
        text = re.sub(r'\s+', ' ', text).strip().title()
    return text
