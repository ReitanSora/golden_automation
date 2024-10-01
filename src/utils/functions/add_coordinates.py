import logging
from pymongo.errors import ConnectionFailure, DuplicateKeyError, OperationFailure
from src.utils.functions.normalize_text import normalize

# Configuración del logger para mejor control de los mensajes de error
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def add_one_coordinate(db, collection_name, country: str, province: str, city: str, lat_prov, lon_prov, lat_city, lon_city):
    try:
        # Verificar la conexión a la base de datos
        db.command("ping")  # Comando simple para verificar la conexión
    except ConnectionFailure:
        logging.error(
            "No se pudo conectar a la base de datos. Verifica la conexión.")
        return

    try:
        # Buscar si ya existe un documento con las mismas coordenadas
        existing_document = db[collection_name].find_one({
            'sub_1': normalize(country),
            'sub_3': normalize(province),
            'lat_sub_3': lat_prov,
            'lon_sub_3': lon_prov,
            'sub_4': normalize(city),
            'lat_sub_4': lat_city,
            'lon_sub_4': lon_city
        })

        # Si no existe un documento con esas coordenadas, insertar uno nuevo
        if not existing_document:
            data = {
                'sub_1': normalize(country),
                'sub_3': normalize(province),
                'lat_sub_3': lat_prov,
                'lon_sub_3': lon_prov,
                'sub_4': normalize(city),
                'lat_sub_4': lat_city,
                'lon_sub_4': lon_city
            }
            try:
                db[collection_name].insert_one(data)
                print("Documento insertado correctamente.")
            except DuplicateKeyError:
                logging.error(
                    "Error: El documento ya existe (clave duplicada).")
            except OperationFailure as e:
                logging.error(f"Fallo de operación en la inserción: {e}")
            except Exception as e:
                logging.error(f"Error inesperado durante la inserción: {e}")
        else:
            print("El documento ya existe en la base de datos.")

    except OperationFailure as e:
        logging.error(f"Error al ejecutar la consulta: {e}")
    except Exception as e:
        logging.error(f"Error inesperado durante la búsqueda: {e}")
