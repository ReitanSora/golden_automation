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
            print(match.group(1))
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

def save_updated_documents(username, doc, platform):
    # Almacenar los datos del registro actualizado
    updated_records.append({
        'username': username,
        '_id': doc['_id'],
        'name': doc['name'],
        'RedSocial': platform
    })

def save_failed_updates(username, platform):
    # Si no se encuentra el documento
    failed_updates.append({
        'username': username,
        'RedSocial': platform,
        'error': 'Documento no encontrado'
    })

def update_document(collection_name, field_name, username, update_data):
    db[f'{collection_name}'].update_one(
        {f'{field_name}': username},
        {'$set': update_data},
        upsert=False
    )

def extract_id_facebook(url):
    id_facebook = url.split("/profile.php?id=")[-1]
    find_result = list(db['localfacebook'].find({'_id': id_facebook}))
    return find_result[0]['username']

def update():
    # Leer el archivo Excel
    df = pd.read_excel('./storage/Peru.xlsx')

    # Filtrar las columnas que necesitamos del Excel
    df_filtered = df[['Scan FB', 'Scan IG', 'Scan TW', 'Scan YT', 'Scan TK', 'Departamento', 'Provincia', 'Distrito',
                      'URL Facebook', 'URL Instagram', 'URL Twitter', 'URL YouTube', 'URL TikTok']]


    # Recorremos cada fila del DataFrame filtrado
    for index, row in df_filtered.iterrows():

        try:

            # Normalizar los valores de Departamento, Provincia y Distrito
            row['Departamento'] = normalize_text(row['Departamento'])
            row['Provincia'] = normalize_text(row['Provincia'])
            row['Distrito'] = normalize_text(row['Distrito'])

            if row['Departamento'] not in department_iso.keys():
                print(f'Departamento excel: {row["Departamento"]}')
                failed_updates.append({
                    'row_index': index,
                    'Departamento': row['Departamento'],
                    'error': 'Departamento no válido'
                })

            if row['Provincia'] not in cities['peru']:
                print(f'Provincia excel: {row['Provincia']}')
                failed_updates.append({
                    'row_index': index,
                    'Provincia': row['Provincia'],
                    'error': 'Provincia no válida'
                })
                continue

            # Comprobamos si alguna columna de Scan tiene "Ingresada"
            if any(row[['Scan FB', 'Scan IG', 'Scan TW', 'Scan YT', 'Scan TK']] == 'Ingresada') and not (
                    pd.isna(row['Departamento']) and pd.isna(row['Provincia']) and pd.isna(row['Distrito'])):

                # Extraemos los usernames de las redes sociales que tengan "Ingresada" en Scan
                fb_username = extract_username(
                    row['URL Facebook'], 'facebook') if row['Scan FB'] == 'Ingresada' else None
                if fb_username.strip() == 'profile.php':
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
                            save_updated_documents(username, find_result[0], f'{platform_name}')
                            update_document(f'{collection_name}', f'{field_name}',username, update_data)
                        else:
                            save_failed_updates(username, f'{platform_name}')

                # Procesar actualizaciones para cada red social
                process_update('localfacebook', 'username', fb_username, 'Facebook')
                process_update('instagram', 'username', ig_username, 'Instagram')
                process_update('twitter', 'screenName', tw_username, 'Twitter')
                process_update('youtube', '_id', yt_username, 'YouTube')
                process_update('tiktok', 'username', tk_username, 'TikTok')

        except Exception as e:
            # Si ocurre un error, almacenamos el índice de la fila y el error en el array de fallos
            failed_updates.append({'row_index': index, 'error': str(e)})

    # Convertir los arrays a DataFrames
    df_updated = pd.DataFrame(updated_records)
    df_failed = pd.DataFrame(failed_updates)

    # Guardar los DataFrames en archivos Excel con información detallada antes y después de la ejecución
    df_updated.to_excel('./storage/logs/registros_actualizados.xlsx', index=False)
    df_failed.to_excel('./storage/logs/registros_fallidos.xlsx', index=False)
