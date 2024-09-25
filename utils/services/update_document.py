import pandas as pd
import json
from config import mongo, excel
from pymongo import MongoClient

from ..functions.export_to_xlsx import export_xlsx
from ..functions.xlsx_to_df import import_xlsx
from ..functions.validate_update_data import validate
from ..functions.extract_username import extract
from ..functions.normalize_text import normalize
from ..functions.update_one_mongodb import update_one

# Diccionario con los codigos ISO de Perú
with open("./storage/localization/iso.json", "r") as f:
    department_iso = json.load(f)

# Diccionario con las ciudades de Perú
with open("./storage/localization/city.json", "r") as f:
    cities = json.load(f)

# Arrays para almacenar los registros modificados y los que fallaron
updated_records = []
failed_updates = []

client = MongoClient(mongo['mongodb_url'])
database_name = client[mongo['mongodb_db_name']]


def save_updated_documents(username='N.A', doc=None, platform='N.A', subzone_2=None, subzone_3=None, subzone_4=None, subzone_5=None, contextA='N.A', typeA='N.A', desc='N.A'):
    # Almacenar los datos del registro actualizado
    new_item = {'_id': doc.get('_id'),
                'name': doc.get('name'),
                'username': username,
                'RedSocial': platform,
                f'{excel['excel_subzone_2']}_before': doc.get('region'),
                f'{excel['excel_subzone_3']}_before': doc.get('prov'),
                f'{excel['excel_subzone_4']}_before': doc.get('city'),
                f'{excel['excel_subzone_5']}_before': doc.get('parish'),
                'contextA_before': doc.get('contextA'),
                'typeA_before': doc.get('typeA'),
                'desc_before': doc.get('desc'),
                f'{excel['excel_subzone_2']}_after': subzone_2 if subzone_2 != None else doc.get('region'),
                f'{excel['excel_subzone_3']}_after': subzone_3,
                f'{excel['excel_subzone_4']}_after': subzone_4,
                f'{excel['excel_subzone_5']}_after': subzone_5,
                'contextA_after': contextA,
                'typeA_after': typeA,
                'desc_after': desc,
                }
    updated_records.append(new_item)
    del new_item


def save_failed_updates(index, subzone_2=None, subzone_3=None, subzone_4=None, subzone_5=None, username='N.A', platform='N.A', fail_error='N.A', contextA=None, typeA=None, desc='N.A'):
    # Si no se encuentra el documento
    new_item = {
        'Índice excel': index,
        'Username': username,
        'Red Social': platform,
        'Categoría Facebook': contextA,
        'Categoria/Criterio': typeA,
        excel['excel_subzone_2']: subzone_2,
        excel['excel_subzone_3']: subzone_3,
        excel['excel_subzone_4']: subzone_4,
        excel['excel_subzone_5']: subzone_5,
        'Descripción': desc,
        'Error': f'{fail_error}'
    }
    failed_updates.append(new_item)
    del new_item


def extract_id_facebook(url):
    id_facebook = url.split("/profile.php?id=")[-1]
    find_result = list(database_name[excel['mongodb_fb_collection']
                                     ].find({'_id': id_facebook}))
    return find_result[0].get('username') if len(find_result) > 0 else f'{id_facebook}'


def update():
    df_filtered = import_xlsx()

    sub2_present = excel['excel_subzone_2'] in df_filtered.columns

    # Recorremos cada fila del DataFrame filtrado
    for index, row in df_filtered.iterrows():

        try:

            row[excel['excel_subzone_2']] = normalize(
                row[excel['excel_subzone_2']]) if sub2_present else None
            row[excel['excel_subzone_3']] = normalize(
                row[excel['excel_subzone_3']])
            row[excel['excel_subzone_4']] = normalize(
                row[excel['excel_subzone_4']])
            row[excel['excel_subzone_5']] = normalize(
                row[excel['excel_subzone_5']])
            row['Categoria/Criterio'] = normalize(
                row['Categoria/Criterio'])

            if sub2_present and row[excel['excel_subzone_2']] not in department_iso.keys():
                save_failed_updates(index=index + 2, subzone_2=row[excel['excel_subzone_2']], subzone_3=row[excel['excel_subzone_3']], subzone_4=row[excel['excel_subzone_4']],
                                    subzone_5=row[excel['excel_subzone_5']], contextA=row['Categoría Facebook'], typeA=row['Categoria/Criterio'], fail_error=f'{excel['excel_subzone_2']} no válido')

            if row[excel['excel_subzone_3']] not in department_iso.keys():
                save_failed_updates(index=index + 2, subzone_2=row[excel['excel_subzone_2']], subzone_3=row[excel['excel_subzone_3']], subzone_4=row[excel['excel_subzone_4']],
                                    subzone_5=row[excel['excel_subzone_5']], contextA=row['Categoría Facebook'], typeA=row['Categoria/Criterio'], fail_error='Subnivel 3 no válido')

            if row[excel['excel_subzone_4']] not in cities['peru']:
                save_failed_updates(index=index + 2, subzone_2=row[excel['excel_subzone_2']], subzone_3=row[excel['excel_subzone_3']], subzone_4=row[excel['excel_subzone_4']],
                                    subzone_5=row[excel['excel_subzone_5']], contextA=row['Categoría Facebook'], typeA=row['Categoria/Criterio'], fail_error='Subnivel 4 no válido')
                continue

            # Comprobamos si alguna columna de Scan tiene "Ingresada"
            if any(row[['Scan FB', 'Scan IG', 'Scan TW', 'Scan YT', 'Scan TK']] == 'Ingresada') and not (
                    pd.isna(row[excel['excel_subzone_2']]) and pd.isna(row[excel['excel_subzone_3']]) and pd.isna(row[excel['excel_subzone_4']]) and pd.isna(row[excel['excel_subzone_5']])):

                # Extraemos los usernames de las redes sociales que tengan "Ingresada" en Scan
                fb_username = extract(
                    row['URL Facebook'], 'facebook') if row['Scan FB'] == 'Ingresada' else None
                if fb_username == 'profile.php':
                    fb_username = extract_id_facebook(row['URL Facebook'])
                ig_username = extract(
                    row['URL Instagram'], 'instagram') if row['Scan IG'] == 'Ingresada' else None
                tw_username = extract(
                    row['URL Twitter'], 'twitter') if row['Scan TW'] == 'Ingresada' else None
                if pd.isna(row['URL Twitter']):
                    row['URL Twitter'] = ''
                if row['URL Twitter'][:1] == '@':
                    tw_username = row['URL Twitter'][1:]
                yt_username = extract(
                    row['URL YouTube'], 'youtube') if row['Scan YT'] == 'Ingresada' else None
                tk_username = extract(
                    row['URL TikTok'], 'tiktok') if row['Scan TK'] == 'Ingresada' else None

                # campos a actualizar
                update_data = validate(sub2_present, row, department_iso)

                def process_update(collection_name, field_name, username, platform_name):
                    if username:
                        find_result = list(database_name[f'{collection_name}'].find(
                            {f'{field_name}': username}))
                        if len(find_result) > 0:
                            save_updated_documents(username=username, doc=find_result[0],
                                                   platform=f'{platform_name}', subzone_2=row[excel['excel_subzone_2']], subzone_3=row[excel['excel_subzone_3']], subzone_4=row[excel['excel_subzone_4']], subzone_5=row[excel['excel_subzone_5']], contextA=row['Categoría Facebook'], typeA=row['Categoria/Criterio'], desc=row['Descripción Facebook'])
                            update_one(database_name, f'{collection_name}',
                                       f'{field_name}', username, update_data)
                        else:
                            save_failed_updates(index=index+2, username=username,
                                                platform=f'{platform_name}', fail_error='Usuario no encontrado en la bd')

                # Procesar actualizaciones para cada red social
                process_update(mongo['mongodb_fb_collection'], mongo['mongodb_fb_field_name'],
                               fb_username, 'Facebook')
                process_update(mongo['mongodb_ig_collection'], mongo['mongodb_ig_field_name'],
                               ig_username, 'Instagram')
                process_update(mongo['mongodb_tw_collection'], mongo['mongodb_tw_field_name'],
                               tw_username, 'Twitter')
                process_update(mongo['mongodb_yt_collection'], mongo['mongodb_yt_field_name'],
                               yt_username, 'YouTube')
                process_update(mongo['mongodb_tk_collection'], mongo['mongodb_tk_field_name'],
                               tk_username, 'TikTok')

        except Exception as e:
            save_failed_updates(index=index+2, fail_error=f'{e}')

    export_xlsx(updated_records, failed_updates)
    print('Realizado exitosamente')
