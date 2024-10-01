import requests
from src.utils.functions.normalize_text import normalize

# Para insertar nuevas coordenadas en la base de datos
from src.utils.functions.add_coordinates import add_one_coordinate

# registrarse en https://www.openstreetmap.org/
# Función para obtener coordenadas desde OpenStreetMap


def get_coordinates_osm(direction: str):
    url = f"https://nominatim.openstreetmap.org/search?q={
        direction}&format=json&limit=1"

    headers = {
        # Cambiar a correo resgistrado, nombre cualquiera
        'User-Agent': 'Localizacion (su correo aquí)'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            latitud = data[0]['lat']
            longitud = data[0]['lon']
            return latitud, longitud
        else:
            return None, None
    else:
        print(f"Error al realizar la solicitud HTTP: {response.status_code}")
        return None, None


# Función principal para obtener las coordenadas de provincia y ciudad
def obtener_coordenadas(db, collection_name, country: str, province: str, city: str):
    # Buscar en la colección si ya existen las coordenadas
    existing_coords = db[collection_name].find_one({
        'sub_1': normalize(country),
        'sub_3': normalize(province),
        'sub_4': normalize(city)
    })

    if existing_coords:
        # Si existen las coordenadas, retornarlas sin hacer la llamada al API
        print(f"Coordenadas encontradas en la base de datos para {
              province}, {city}.")
        return existing_coords['lat_sub_3'], existing_coords['lon_sub_3'], existing_coords['lat_sub_4'], existing_coords['lon_sub_4']
    else:
        # Si no existen las coordenadas, llamar al API
        print(f"Coordenadas no encontradas en la base de datos. Consultando el API para {
              province}, {city}.")
        province_direction = f"{country}, {province}"
        city_direction = f"{country}, {city}"

        # Obtener coordenadas de la provincia y la ciudad
        province_lat, province_lon = get_coordinates_osm(province_direction)
        city_lat, city_lon = get_coordinates_osm(city_direction)

        # Verificar si se obtuvieron correctamente las coordenadas antes de insertarlas
        if province_lat and province_lon and city_lat and city_lon:
            # Insertar las coordenadas en la base de datos
            add_one_coordinate(db, collection_name, country, province,
                               city, province_lat, province_lon, city_lat, city_lon)
            return province_lat, province_lon, city_lat, city_lon
        else:
            print(f"No se pudieron obtener las coordenadas del API para {
                  province}, {city}.")
            return None, None, None, None
