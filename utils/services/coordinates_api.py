import requests


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
def obtener_coordenadas(country: str, province: str, city: str):

    # Obtener coordenadas de la provincia
    province_direction = f"{country}, {province}"
    province_lat, province_lon = get_coordinates_osm(province_direction)

    # Obtener coordenadas de la ciudad
    city_direction = f"{country}, {city}"
    city_lat, city_lon = get_coordinates_osm(city_direction)

    return province_lat, province_lon, city_lat, city_lon
