import pytest
from unittest.mock import MagicMock  # Importamos MagicMock para simular objetos
# Importamos la función a probar
from src.services.coordinates_api import obtener_coordenadas


def test_obtener_coordenadas():
    """Prueba para la función obtener_coordenadas.

    Esta prueba verifica que la función retorne las coordenadas
    correctas cuando se encuentran en la base de datos.

    Utiliza un objeto MagicMock para simular la base de datos.

    Args:
        None
    """
    db = MagicMock()  # Creamos un objeto simulado para la base de datos
    collection = db['coordinates']  # Simulamos la colección 'coordinates'

    # Simulamos que la consulta devuelve un documento con coordenadas
    collection.find_one.side_effect = [
        {"lat_sub_3": 12.34, "lon_sub_3": 56.78,
            "lat_sub_4": 12.34, "lon_sub_4": 56.78},
    ]

    lat_prov, lon_prov, lat_city, lon_city = obtener_coordenadas(
        db, 'coordinates', "subnivel_1", "subnivel_3", "subnivel_4")

    # Verificamos que la latitud de subnivel 3 sea correcta.
    assert lat_prov == 12.34
    # Verificamos que la longitud de subnivel 3 sea correcta.
    assert lon_prov == 56.78
    # Verificamos que la latitud de subnivel 4 sea correcta.
    assert lat_city == 12.34
    # Verificamos que la longitud de subnivel 4 sea correcta.
    assert lon_city == 56.78


def test_obtener_coordenadas_no_results():
    """Prueba para la función obtener_coordenadas cuando no hay resultados.

    Esta prueba verifica que la función retorne None para todas
    las coordenadas cuando no se encuentran en la base de datos.

    Utiliza un objeto MagicMock para simular la base de datos.

    Args:
        None
    """
    db = MagicMock()  # Creamos un objeto simulado para la base de datos
    collection = db['coordinates']  # Simulamos la colección 'coordinates'

    # Simulamos que no se encuentran resultados en la consulta
    collection.find_one.side_effect = [None]

    lat_prov, lon_prov, lat_city, lon_city = obtener_coordenadas(
        db, 'coordinates', "subnivel_1", "subnivel_3", "subnivel_4")

    # Verificamos que la latitud de subnivel 3 sea None.
    assert lat_prov is None
    # Verificamos que la longitud de subnivel 3 sea None.
    assert lon_prov is None
    # Verificamos que la latitud de subnivel 4 sea None.
    assert lat_city is None
    # Verificamos que la longitud de subnivel 4 sea None.
    assert lon_city is None
