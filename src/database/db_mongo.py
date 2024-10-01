from pymongo import MongoClient
from config import mongo


def get_database():
    """
    Establece una conexión con la base de datos MongoDB y retorna la instancia de la base de datos.

    Returns:
        database: La instancia de la base de datos configurada en el archivo de configuración.
    """
    client = MongoClient(
        # Crea un cliente MongoDB utilizando la URL de conexión.
        mongo['mongodb_url'])
    # Obtiene la base de datos especificada en la configuración.
    database = client[mongo['mongodb_db_name']]
    return database  # Retorna la instancia de la base de datos.


def get_coordinates_collection():
    """
    Obtiene la colección de coordenadas desde la base de datos MongoDB.

    Returns:
        collection: La colección de coordenadas dentro de la base de datos.
    """
    database = get_database(
        # Llama a la función get_database para obtener la instancia de la base de datos.
    )
    # Retorna la colección de coordenadas.
    return database[mongo['mongodb_db_name_coordinates']]
