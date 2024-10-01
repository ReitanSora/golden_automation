import pytest
from unittest.mock import patch  # Importamos patch para simular funciones


def test_root_route(client):
    """Prueba para la ruta raíz de la aplicación.

    Esta prueba verifica que la ruta principal ('/') devuelva un
    estado de éxito (200) y el contenido correcto.

    Args:
        client: El cliente de prueba que se usa para realizar la solicitud.
    """
    response = client.get('/')  # Realizamos una solicitud GET a la ruta raíz.
    # Comprobamos que el código de estado sea 200 (éxito).
    assert response.status_code == 200
    # Verificamos que el contenido de la respuesta sea 'root'.
    assert response.data == b'root'


# Simulamos la función obtener_coordenadas
@patch('src.routes.coord_routes.obtener_coordenadas')
def test_get_coordinates_success(mock_obtener_coordenadas, client):
    """Prueba para obtener coordenadas exitosamente.

    Esta prueba verifica que la ruta '/obtener-coordenadas'
    devuelva las coordenadas correctas cuando se le pasan los
    parámetros requeridos.

    Args:
        mock_obtener_coordenadas: Simulación de la función que obtiene coordenadas.
        client: El cliente de prueba que se usa para realizar la solicitud.
    """
    # Simulamos que la función devuelve coordenadas específicas
    mock_obtener_coordenadas.return_value = (12.34, 56.78, 12.34, 56.78)

    response = client.get(
        '/obtener-coordenadas?subnivel_1=test1&subnivel_3=test3&subnivel_4=test4')

    assert response.status_code == 200  # Verificamos que el estado sea 200.
    assert response.json == {  # Verificamos que la respuesta contenga las coordenadas correctas.
        "lat_subnivel_3": 12.34,
        "lon_subnivel_3": 56.78,
        "lat_subnivel_4": 12.34,
        "lon_subnivel_4": 56.78
    }


def test_get_coordinates_missing_params(client):
    """Prueba para obtener coordenadas con parámetros faltantes.

    Esta prueba verifica que la ruta '/obtener-coordenadas' devuelva un
    error 400 cuando no se proporcionan todos los parámetros necesarios.

    Args:
        client: El cliente de prueba que se usa para realizar la solicitud.
    """
    response = client.get(
        '/obtener-coordenadas?subnivel_1=test1&subnivel_3=test3')

    # Verificamos que el estado sea 400 (error por falta de parámetros).
    assert response.status_code == 400
    assert response.json == {  # Verificamos que el mensaje de error sea el correcto.
        "error": "Faltan parámetros: subnivel_1, subnivel_3, subnivel_4 son requeridos"
    }


# Simulamos la función obtener_coordenadas
@patch('src.routes.coord_routes.obtener_coordenadas')
def test_get_coordinates_no_coords(mock_obtener_coordenadas, client):
    """Prueba para la obtención de coordenadas cuando no hay resultados.

    Esta prueba verifica que la ruta '/obtener-coordenadas' devuelva un
    error 500 cuando no se pueden obtener coordenadas.

    Args:
        mock_obtener_coordenadas: Simulación de la función que obtiene coordenadas.
        client: El cliente de prueba que se usa para realizar la solicitud.
    """
    # Simulamos que la función no devuelve coordenadas
    mock_obtener_coordenadas.return_value = (None, None, None, None)

    response = client.get(
        '/obtener-coordenadas?subnivel_1=test1&subnivel_3=test3&subnivel_4=test4')

    # Verificamos que el estado sea 500 (error interno del servidor).
    assert response.status_code == 500
    # Verificamos el mensaje de error.
    assert response.json == {"error": "No se pudieron obtener las coordenadas"}
