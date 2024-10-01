from decouple import config


def save_updated_documents(username='N.A', doc=None, platform='N.A', subzone_2=None, subzone_3=None, subzone_4=None, subzone_5=None, contextA='N.A', typeA='N.A', desc='N.A', latitude_prov='N.A', longitude_prov='N.A', latitude_city='N.A', longitude_city='N.A',updated=[]):
    # Almacenar los datos del registro actualizado
    new_item = {'_id': doc.get('_id'),
                'name': doc.get('name'),
                'username': username,
                'RedSocial': platform,
                f'{config('EXCEL_SUBZONE_2')}_before': doc.get('region'),
                f'{config('EXCEL_SUBZONE_3')}_before': doc.get('prov'),
                f'{config('EXCEL_SUBZONE_4')}_before': doc.get('city'),
                f'{config('EXCEL_SUBZONE_5')}_before': doc.get('parish'),
                'contextA_before': doc.get('contextA'),
                'typeA_before': doc.get('typeA'),
                'desc_before': doc.get('desc'),
                'lat_prov_before': doc.get('lat_prov'),
                'lon_prov_before': doc.get('lon_prov'),
                'lat_city_before': doc.get('lat_city'),
                'lon_city_before': doc.get('lon_city'),
                f'{config('EXCEL_SUBZONE_2')}_after': subzone_2 if subzone_2 != None else doc.get('region'),
                f'{config('EXCEL_SUBZONE_3')}_after': subzone_3,
                f'{config('EXCEL_SUBZONE_4')}_after': subzone_4,
                f'{config('EXCEL_SUBZONE_5')}_after': subzone_5,
                'contextA_after': contextA,
                'typeA_after': typeA,
                'desc_after': desc,
                'lat_prov_after': latitude_prov,
                'lon_prov_after': longitude_prov,
                'lat_city_after': latitude_city,
                'lon_city_after': longitude_city,
                }
    updated.append(new_item)
    del new_item


def save_failed_updates(index, subzone_2=None, subzone_3=None, subzone_4=None, subzone_5=None, username='N.A', platform='N.A', fail_error='N.A', contextA=None, typeA=None, desc='N.A', failed=[]):
    # Si no se encuentra el documento
    new_item = {
        'Índice excel': index,
        'Username': username,
        'Red Social': platform,
        'Categoría Facebook': contextA,
        'Categoria/Criterio': typeA,
        config('EXCEL_SUBZONE_2'): subzone_2,
        config('EXCEL_SUBZONE_3'): subzone_3,
        config('EXCEL_SUBZONE_4'): subzone_4,
        config('EXCEL_SUBZONE_5'): subzone_5,
        'Descripción': desc,
        'Error': f'{fail_error}'
    }
    failed.append(new_item)
    del new_item