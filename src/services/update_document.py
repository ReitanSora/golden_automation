import pandas as pd
import json
from config import mongo, excel
from pymongo import MongoClient

from src.utils.functions.export_to_xlsx import export_xlsx
from src.utils.functions.xlsx_to_df import import_xlsx
from src.utils.functions.validate_update_data import validate
from src.utils.functions.extract_username import extract
from src.utils.functions.normalize_text import normalize
from src.utils.functions.update_one_mongodb import update_one
from src.utils.functions.export_date import export_date
from src.utils.functions.correct_subzone import c_subzone_3, c_subzone_4
from src.utils.functions.validate_date import compare_date
from src.utils.functions.save_logs import *
from src.utils.functions.edit_excel import edit
from src.services.coordinates_api import obtener_coordenadas
from src.services.upload_file import upload_files

# Diccionario con los codigos ISO de Perú y sus Departamentos
with open("./src/storage/localization/iso.json", "r") as f:
    department_iso = json.load(f)

# Diccionario con las ciudades de Perú
with open("./src/storage/localization/city.json", "r") as f:
    cities = json.load(f)

# Arrays para almacenar los registros modificados y los que fallaron
updated_records = []
failed_updates = []

# Conectar a MongoDB usando las variables de entorno
client = MongoClient(mongo['mongodb_url'])
database_name = client[mongo['mongodb_db_name']]  # Base de datos "golden"
collection_name = mongo['mongodb_db_name_coordinates']  # Colección "coordinates"

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

        for col in [excel['excel_subzone_3'], excel['excel_subzone_4'], excel['excel_subzone_5']]:
            if pd.isna(row[col]):
                df_filtered.at[index, col] = ''

        fecha = open('src/storage/date.txt', "r").read()
        
        if pd.isna(row['Fecha']) == False:

            if compare_date(saved_date=fecha, new_date=str(row['Fecha'])):

                try:

                    row[excel['excel_subzone_2']] = row[excel['excel_subzone_2']] if sub2_present else None

                    # Comprobamos si alguna columna de Scan tiene "Ingresada"
                    if any(row[['Scan FB', 'Scan IG', 'Scan TW', 'Scan YT', 'Scan TK']] == 'Ingresada') and not (
                            pd.isna(row[excel['excel_subzone_2']]) and pd.isna(row[excel['excel_subzone_3']]) and pd.isna(row[excel['excel_subzone_4']]) and pd.isna(row[excel['excel_subzone_5']])):

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
                                                subzone_5=row[excel['excel_subzone_5']], contextA=row['Categoría Facebook'], typeA=row['Categoria/Criterio'], fail_error=f'{excel['excel_subzone_2']} no válido', failed=failed_updates)

                        if row[excel['excel_subzone_3']] not in department_iso.keys() and row[excel['excel_subzone_3']] != "NA":
                            # Intentamos corregir el nombre del subnivel 3 usando IA
                            corrected_subzone_3 = c_subzone_3(
                                row[excel['excel_subzone_3']])

                            if corrected_subzone_3 in department_iso.keys():
                                # Si la IA sugiere una corrección válida, actualizamos el nombre del departamento
                                row[excel['excel_subzone_3']
                                    ] = corrected_subzone_3
                            else:
                                # Si la corrección falla, guardamos el registro como fallido
                                save_failed_updates(index=index + 2, subzone_2=row[excel['excel_subzone_2']], subzone_3=row[excel['excel_subzone_3']], subzone_4=row[excel['excel_subzone_4']],
                                                    subzone_5=row[excel['excel_subzone_5']], contextA=row['Categoría Facebook'], typeA=row['Categoria/Criterio'], fail_error=f'{excel['excel_subzone_3']} no válido', failed=failed_updates)
                                continue


                        if row[excel['excel_subzone_4']] not in cities['peru'] and row[excel['excel_subzone_4']] != "NA":
                            # Intentamos corregir el nombre del subnivel 4 usando IA
                            corrected_subzone_4 = c_subzone_4(
                                row[excel['excel_subzone_4']])

                            if (corrected_subzone_4 in cities['peru']):
                                # Si la IA sugiere una corrección válida, actualizamos el nombre del departamento
                                row[excel['excel_subzone_4']
                                    ] = corrected_subzone_4
                            else:
                                save_failed_updates(index=index + 2, subzone_2=row[excel['excel_subzone_2']], subzone_3=row[excel['excel_subzone_3']], subzone_4=row[excel['excel_subzone_4']],
                                                    subzone_5=row[excel['excel_subzone_5']], contextA=row['Categoría Facebook'], typeA=row['Categoria/Criterio'], fail_error=f'{excel['excel_subzone_4']} no válido', failed=failed_updates)
                                continue

                        if row[excel['excel_subzone_2']] != None:
                            df_filtered.at[index, excel['excel_subzone_2']] = row[excel['excel_subzone_2']]
                        df_filtered.at[index, excel['excel_subzone_3']] = row[excel['excel_subzone_3']]
                        df_filtered.at[index, excel['excel_subzone_4']] = row[excel['excel_subzone_4']]
                        df_filtered.at[index, excel['excel_subzone_5']] = row[excel['excel_subzone_5']]

                        # Extraemos los usernames de las redes sociales que tengan "Ingresada" en Scan
                        fb_username = extract(
                            row['URL Facebook'], 'facebook') if row['Scan FB'] == 'Ingresada' else None
                        if fb_username == 'profile.php':
                            fb_username = extract_id_facebook(
                                row['URL Facebook'])
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
                        
                        lat_prov, lon_prov, lat_city, lon_city = obtener_coordenadas(database_name, collection_name, str(excel['file_name'][:-5]), row[excel['excel_subzone_3']], row[excel['excel_subzone_4']])
                        
                        # campos a actualizar
                        update_data = validate(
                            sub2_present,
                            row,
                            department_iso,
                            lat_prov,
                            lon_prov,
                            lat_city,
                            lon_city
                            )

                        def process_update(collection_name, field_name, username, platform_name):
                            if username:
                                find_result = list(database_name[f'{collection_name}'].find(
                                    {f'{field_name}': username}))
                                if len(find_result) > 0:
                                    save_updated_documents(username=username,
                                                           doc=find_result[0],
                                                           platform=f'{platform_name}',
                                                           subzone_2=row[excel['excel_subzone_2']],
                                                           subzone_3=row[excel['excel_subzone_3']],
                                                           subzone_4=row[excel['excel_subzone_4']],
                                                           subzone_5=row[excel['excel_subzone_5']],
                                                           contextA=row['Categoría Facebook'],
                                                           typeA=row['Categoria/Criterio'],
                                                           desc=row['Descripción Facebook'],
                                                           latitude_prov=lat_prov,
                                                           longitude_prov=lon_prov,
                                                           latitude_city=lat_city,
                                                           longitude_city=lon_city,
                                                           updated=updated_records)
                                    update_one(database_name, f'{collection_name}',
                                               f'{field_name}', username, update_data)
                                else:
                                    save_failed_updates(index=index+2,
                                                        username=username,
                                                        platform=f'{platform_name}',
                                                        fail_error='Usuario no encontrado en la bd',
                                                        failed=failed_updates)

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

                    else:
                        save_failed_updates(index=index+2,
                                            fail_error='No ha sido ingresado en Scan/ No posee ubicación',
                                            failed=failed_updates)
                except Exception as e:
                    save_failed_updates(index=index+2,
                                        fail_error=f'{e}',
                                        failed=failed_updates)

        else:
            save_failed_updates(index=index + 2,
                                fail_error='No cuenta con una fecha',
                                failed=failed_updates)
    
    export_xlsx(updated_records, failed_updates)
    export_date()
    edit( sub2_present, df_filtered)
    upload_files()
    print('Realizado exitosamente')
