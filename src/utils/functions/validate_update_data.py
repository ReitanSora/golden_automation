def validate(row_present: bool, row, department_iso, lat_prov, lon_prov, lat_city, lon_city):

    if row_present:
        update_data = {
            'region': row['Subnivel 2'],
            'prov': row['Subnivel 3'],
            'city': row['Subnivel 4'],
            'parish': row['Subnivel 5'],
            'provIso': department_iso.get(row['Subnivel 3'], ''),
            'contextA': row['Categoría Facebook'].strip(),
            'typeA': row['Categoria/Criterio'],
            'desc': row['Descripción Facebook'],
            'lat_prov': lat_prov,
            'lon_prov': lon_prov,
            'lat_city': lat_city,
            'lon_city': lon_city
        }
    else:
        update_data = {
            'prov': row['Subnivel 3'],
            'city': row['Subnivel 4'],
            'parish': row['Subnivel 5'],
            'provIso': department_iso.get(row['Subnivel 3'], ''),
            'contextA': row['Categoría Facebook'].strip(),
            'typeA': row['Categoria/Criterio'],
            'desc': row['Descripción Facebook'],
            'lat_prov': lat_prov,
            'lon_prov': lon_prov,
            'lat_city': lat_city,
            'lon_city': lon_city
        }

    return update_data
