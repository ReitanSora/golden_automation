import pytest
# Importamos la aplicación Flask desde el archivo principal
from main import initialize_app as flask_app


@pytest.fixture
def app():
    """Fixture para la aplicación Flask.

    Este es un 'fixture' de pytest que configura y proporciona una
    instancia de la aplicación Flask para las pruebas. Un 'fixture'
    es un mecanismo que permite configurar condiciones específicas
    antes de que se ejecute una prueba. En este caso, se usa para
    asegurar que la aplicación esté disponible.

    Yield:
        app: La instancia de la aplicación Flask para usar en las pruebas.
    """
    yield flask_app  # La aplicación se entrega a las pruebas, y al finalizar, se cierra.


@pytest.fixture
def client(app):
    """Fixture para el cliente de prueba.

    Este 'fixture' crea un cliente de prueba a partir de la
    aplicación Flask. El cliente de prueba permite simular
    peticiones HTTP a la aplicación, como si fueran usuarios
    reales interactuando con ella.

    Args:
        app: La instancia de la aplicación Flask proporcionada por el
             'fixture' anterior.

    Returns:
        test_client: Un cliente que se puede usar para realizar
                     peticiones HTTP a la aplicación.
    """
    return app.test_client()  # Devuelve un cliente de prueba para hacer solicitudes.
