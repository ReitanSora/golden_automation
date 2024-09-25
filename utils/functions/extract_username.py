import re
import pandas as pd


# Función para extraer el username de una URL según la red social
def extract(url, platform):
    if pd.isna(url):  # Verificamos si la URL es NaN (vacía)
        return None
    try:
        if platform == 'facebook':
            match = re.search(r'facebook\.com\/([A-Za-z0-9_.-]+)', url)
        elif platform == 'instagram':
            match = re.search(r'instagram\.com\/([A-Za-z0-9_.-]+)', url)
        elif platform == 'twitter':
            # Para URLs de Twitter, el username puede estar después de 'x.com/' o ser una mención '@'
            # Ejemplos:
            # https://x.com/americatv_peru
            # @exitosape
            # El username puede tener caracteres alfanuméricos, guiones y puntos
            match = re.search(
                r'x\.com\/([A-Za-z0-9_.-]+)|\@([A-Za-z0-9_.-]+)', url)
            # Buscamos el username en la URL utilizando la expresión regular para Twitter
            # Consideramos tanto el formato de URL como el de mención
        elif platform == 'youtube':
            # Para URLs de YouTube, el username puede estar en varias formas:
            # 1. Después de 'channel/'
            # 2. Después de 'c/'
            # 3. Después de 'user/'
            # Ejemplos:
            # https://www.youtube.com/channel/UCTTXPfz9eONBspLvdEaCg2g/
            # https://www.youtube.com/c/UCksV2nYo_YnmGTlm9od5gMg
            # https://www.youtube.com/user/UCksV2nYo_YnmGTlm9od5gMg
            # El username puede tener caracteres alfanuméricos, guiones y puntos
            match = re.search(
                r'youtube\.com\/(?:channel\/|c\/|user\/)?([A-Za-z0-9_.-]+)', url)
            # Buscamos el username en la URL utilizando la expresión regular para YouTube
            # Consideramos todos los formatos posibles de URL
        elif platform == 'tiktok':
            match = re.search(r'tiktok\.com\/@([A-Za-z0-9_.-]+)', url)
        if match:
            return match.group(1)  # Retornar el username extraído
        return None
    except Exception as e:
        return None
