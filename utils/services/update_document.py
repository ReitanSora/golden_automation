import traceback

import pandas as pd
import json
import re
import unicodedata
from config import mongo
from pymongo import MongoClient

#Diccionario con los codigos ISO de Perú
with open("./storage/country_iso/pe_iso.json", "r") as f:
    department_iso = json.load(f)

#Diccionario con las ciudades de Perú
with open("./storage/country_iso/city.json", "r") as f:
    cities = json.load(f)

# Arrays para almacenar los registros modificados y los que fallaron
updated_records = []
failed_updates = []

client = MongoClient(mongo['mongodb_url'])
db = client[mongo['mongodb_db_name']]

# Función para extraer el username de una URL según la red social
def extract_username(url, platform):
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
            match = re.search(r'x\.com\/([A-Za-z0-9_.-]+)|@([A-Za-z0-9_.-]+)', url)
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
            match = re.search(r'youtube\.com\/(?:channel\/|c\/|user\/)?([A-Za-z0-9_.-]+)', url)
            # Buscamos el username en la URL utilizando la expresión regular para YouTube
            # Consideramos todos los formatos posibles de URL
        elif platform == 'tiktok':
            match = re.search(r'tiktok\.com\/@([A-Za-z0-9_.-]+)', url)
        if match:
            return match.group(1)  # Retornar el username extraído
        return None
    except Exception as e:
        print(f"Error al extraer username de {platform}: {e}")
        return None

# Función para eliminar tildes y normalizar cadenas
def normalize_text(text):
    if not pd.isna(text):  # Verificamos si el texto es válido
        # Eliminar tildes
        text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
        # Eliminar espacios innecesarios
        text = re.sub(r'\s+', ' ', text).strip().title()
    return text

def save_updated_documents(username = 'N.A', doc = None, platform = 'N.A', row_1 = None, row_2 = None, row_3 = None):
    # Almacenar los datos del registro actualizado
    new_item = {'_id': doc.get('_id'),
            'name': doc.get('name'),
            'username': username,
            'RedSocial': platform,
            'Province_before': doc.get('prov'),
            'City_before': doc.get('city'),
            'Parish_before': doc.get('parish'),
            'Province_after': row_1,
            'City_after': row_2,
            'Parish_after': row_3}
    updated_records.append(new_item)
    del new_item

def save_failed_updates(index, zone_1 = None, zone_2 = None, zone_3 = None, username = 'N.A', platform = 'N.A', fail_error = 'N.A'):
    # Si no se encuentra el documento
    new_item = {
        'Índice excel': index,
        'Username': username,
        'Red Social': platform,
        'Departamento': zone_1,
        'Provincia': zone_2,
        'Distrito': zone_3,
        'Error': f'{fail_error}'
    }
    failed_updates.append(new_item)
    del new_item

def update_document(collection_name, field_name, username, update_data):
    db[f'{collection_name}'].update_one(
        {f'{field_name}': username},
        {'$set': update_data},
        upsert=False
    )

def extract_id_facebook(url):
    id_facebook = url.split("/profile.php?id=")[-1]
    find_result = list(db['localfacebook'].find({'_id': id_facebook}))
    return find_result[0].get('username') if len(find_result) > 0 else f'{id_facebook}'


def update():
    # Leer el archivo Excel
    df = pd.read_excel('./storage/Peru.xlsx')

    # Filtrar las columnas que necesitamos del Excel
    df_filtered = df[['Scan FB', 'Scan IG', 'Scan TW', 'Scan YT', 'Scan TK', 'Departamento', 'Provincia', 'Distrito',
                      'URL Facebook', 'URL Instagram', 'URL Twitter', 'URL YouTube', 'URL TikTok']]
    del df

    # Recorremos cada fila del DataFrame filtrado
    for index, row in df_filtered.iterrows():

        try:

            # Normalizar los valores de Departamento, Provincia y Distrito
            row['Departamento'] = normalize_text(row['Departamento'])
            row['Provincia'] = normalize_text(row['Provincia'])
            row['Distrito'] = normalize_text(row['Distrito'])

            if row['Departamento'] not in department_iso.keys():
                save_failed_updates(index=index + 2, zone_1=row['Departamento'], zone_2=row['Provincia'],
                                    zone_3=row['Distrito'], fail_error='Departamento no válido')

            if row['Provincia'] not in cities['peru']:
                save_failed_updates(index = index+2,zone_1=row['Departamento'], zone_2=row['Provincia'],
                                    zone_3=row['Distrito'], fail_error='Provincia no válida')
                continue

            # Comprobamos si alguna columna de Scan tiene "Ingresada"
            if any(row[['Scan FB', 'Scan IG', 'Scan TW', 'Scan YT', 'Scan TK']] == 'Ingresada') and not (
                    pd.isna(row['Departamento']) and pd.isna(row['Provincia']) and pd.isna(row['Distrito'])):

                # Extraemos los usernames de las redes sociales que tengan "Ingresada" en Scan
                fb_username = extract_username(
                    row['URL Facebook'], 'facebook') if row['Scan FB'] == 'Ingresada' else None
                if fb_username == 'profile.php':
                    fb_username = extract_id_facebook(row['URL Facebook'])
                ig_username = extract_username(
                    row['URL Instagram'], 'instagram') if row['Scan IG'] == 'Ingresada' else None
                tw_username = extract_username(
                    row['URL Twitter'], 'twitter') if row['Scan TW'] == 'Ingresada' else None
                yt_username = extract_username(
                    row['URL YouTube'], 'youtube') if row['Scan YT'] == 'Ingresada' else None
                tk_username = extract_username(
                    row['URL TikTok'], 'tiktok') if row['Scan TK'] == 'Ingresada' else None

                # Campos para actualizar: Departamento -> prov, Provincia -> city, Distrito -> parish
                update_data = {
                    'prov': row['Departamento'].strip(),
                    'city': row['Provincia'].strip(),
                    'parish': row['Distrito'].strip(),
                    'provIso': department_iso.get(row['Departamento'], '')
                }

                def process_update(collection_name, field_name, username, platform_name):
                    if username:
                        find_result = list(db[f'{collection_name}'].find({f'{field_name}': username}))
                        if len(find_result) > 0:
                            save_updated_documents(username=username, doc=find_result[0], platform=f'{platform_name}', row_1= row['Departamento'], row_2= row['Provincia'], row_3= row['Distrito'])
                            update_document(f'{collection_name}', f'{field_name}',username, update_data)
                        else:
                            save_failed_updates( index = index+2,username= username, platform=f'{platform_name}', fail_error='Usuario no encontrado en la bd')

                # Procesar actualizaciones para cada red social
                process_update('localfacebook', 'username', fb_username, 'Facebook')
                process_update('instagram', 'username', ig_username, 'Instagram')
                process_update('twitter', 'screenName', tw_username, 'Twitter')
                process_update('youtube', '_id', yt_username, 'YouTube')
                process_update('tiktok', 'username', tk_username, 'TikTok')

        except Exception as e:
            # Si ocurre un error, almacenamos el índice de la fila y el error en el array de fallos
            save_failed_updates(index=index+2,fail_error=f'{traceback.format_exception(e)}')
            pass

    # Convertir los arrays a DataFrames
    df_updated = pd.DataFrame(updated_records)
    df_failed = pd.DataFrame(failed_updates)

    # Guardar los DataFrames en archivos Excel con información detallada antes y después de la ejecución
    df_updated.to_excel('./storage/logs/registros_actualizados.xlsx', index=False)
    df_failed.to_excel('./storage/logs/registros_fallidos.xlsx', index=False)
