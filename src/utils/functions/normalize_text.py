import pandas as pd
import unicodedata
import re

# Función para eliminar tildes y normalizar cadenas


def normalize(text):
    # Verificación de texto inválido
    if pd.isna(text) or text is None:
        return "NA"

    # Convertir a string y eliminar espacios innecesarios
    text_str = str(text).strip()

    # Validaciones adicionales
    if (text_str == "" or
        text_str.isdigit() or
        text_str in ['True', 'False', 'None', 'null','-','NA','Na'] or
        len(text_str) == 1 and not text_str.isalpha() or
            # Verifica que haya al menos un carácter alfanumérico
            not any(char.isalnum() for char in text_str)):
        return "NA"

    # Eliminar tildes
    text_str = unicodedata.normalize('NFD', text_str).encode(
        'ascii', 'ignore').decode('utf-8')

    # Eliminar espacios innecesarios y formatear
    text_str = re.sub(r'\s+', ' ', text_str).strip().title()

    return text_str
