import pytest
from unittest.mock import patch, MagicMock
from src.database.db_mongo import get_database, get_coordinates_collection


@patch('src.database.db_mongo.MongoClient')  # Simulamos el cliente de MongoDB
def test_get_database(mock_mongo_client):
    """Prueba para verificar la conexión a la base de datos MongoDB.

    Esta prueba asegura que la función get_database retorne una instancia de base de datos válida.

    Args:
        mock_mongo_client: Simulación del cliente de MongoDB.
    """
    mock_db = MagicMock()  # Simulamos la base de datos
    # Simulamos la base de datos
    mock_mongo_client.return_value.__getitem__.return_value = mock_db

    db = get_database()
    # Verificamos que se obtenga la base de datos correcta.
    assert db == mock_db


# Simulamos la función get_database
@patch('src.database.db_mongo.get_database')
def test_get_coordinates_collection(mock_get_database):
    """Prueba para verificar que se obtenga la colección de coordenadas.

    Esta prueba asegura que la función get_coordinates_collection retorne la colección correcta.

    Args:
        mock_get_database: Simulación de la función que obtiene la base de datos.
    """
    mock_collection = MagicMock()  # Simulamos la colección
    # Simulamos la colección
    mock_get_database.return_value.__getitem__.return_value = mock_collection

    collection = get_coordinates_collection()
    # Verificamos que se obtenga la colección correcta.
    assert collection == mock_collection
