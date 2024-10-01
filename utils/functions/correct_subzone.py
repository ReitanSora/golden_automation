from config import gpt
from openai import OpenAI
from difflib import get_close_matches
import json

# Diccionario con los codigos ISO de Perú y sus Departamentos
with open("./storage/localization/iso.json", "r") as f:
    department_iso = json.load(f)

# Diccionario con las ciudades de Perú
with open("./storage/localization/city.json", "r") as f:
    cities = json.load(f)


client = OpenAI(api_key=gpt["gpt_api_key"])


def c_subzone_3(departamento: str) -> str:
    """
    Función para corregir el nombre de un departamento del Perú utilizando el modelo de OpenAI.

    Args:
        departamento (str): Nombre del departamento a corregir.

    Returns:
        str: Respuesta del modelo con la corrección del departamento.
    """

    # Lista de departamentos válidos en Perú
    departamentos_validos = department_iso.keys()

    # Función para normalizar y corregir nombres

    def normalize_departamento(departamento: str) -> str:
        # Normaliza el texto, elimina caracteres no deseados y espacios
        normalized = departamento.strip().title()
        return normalized

    # Corregir el departamento ingresado
    departamento_normalizado = normalize_departamento(departamento)

    # Construir el prompt utilizando el departamento como parámetro
    prompt = (f"Corrige el siguiente nombre de departamento del Perú solo si "
              f"estás seguro en más del 60% de confianza y obligatoriamente la corrección propuesta "
              f"está en la lista de departamentos válidos: {
                  departamentos_validos}. "
              f"El nombre a corregir es: '{departamento_normalizado}'.")

    mensajes = [
        {'role': 'system', 'content': 'Proporciona solo el nombre correcto del departamento o "NA" si no hay corrección necesaria.'},
        {"role": "user", "content": prompt}
    ]

    # Generar la respuesta usando el modelo GPT
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Modelo más económico y con mejor capacidad
        messages=mensajes
    )

    # Obtener la respuesta del asistente
    assistant_response = completion.choices[0].message.content.strip()

    # Intentar corregir nombres con similitudes
    close_matches = get_close_matches(
        departamento_normalizado, departamentos_validos, n=1, cutoff=0.6)

    # Agregar un manejo específico para términos conocidos que deben corregirse
    terminos_conocidos = {
        "L1M4": "Lima",
        "L1m": "Lima",
        "Cajarca": "Cajamarca",
        "Lia": "Lima",  # Puedes agregar más términos conocidos si es necesario
        "Tunes": "Tumbes",
        "Callao": "El Callao"
    }

    if departamento_normalizado in terminos_conocidos:
        return terminos_conocidos[departamento_normalizado]

    # Si hay coincidencias cercanas, devolver la mejor coincidencia
    if close_matches:
        return close_matches[0]

    # Validar si la respuesta es un departamento válido
    if assistant_response in departamentos_validos:
        return assistant_response

    return "NA"  # Si la respuesta no es válida, retornar "NA"


def c_subzone_4(provincia: str) -> str:
    """
    Función para corregir el nombre de una provincia del Perú utilizando el modelo de OpenAI.

    Args:
        provincia (str): Nombre de la provincia a corregir.

    Returns:
        str: Respuesta del modelo con la corrección de la provincia.
    """

    # Lista de provincias válidas en Perú
    provincias_validas = cities['peru']

    # Función para normalizar y corregir nombres
    def normalize_provincia(provincia: str) -> str:
        # Normaliza el texto, elimina caracteres no deseados y espacios
        normalized = provincia.strip().title()
        return normalized

    # Corregir la provincia ingresada
    provincia_normalizada = normalize_provincia(provincia)

    # Construir el prompt utilizando la provincia como parámetro

    # Construir el prompt utilizando la provincia como parámetro
    prompt = (f"Corrige el siguiente nombre de provincia del Perú solo si "
              f"estás seguro en más del 60% de confianza y obligatoriamente la corrección propuesta "
              f"está en la lista de provincias válidas: {
                  provincias_validas}. "
              f"El nombre a corregir es: '{provincia_normalizada}'.")

    mensajes = [
        {'role': 'system', 'content': 'Dame la respuesta explícitamente en la cantidad de palabras que contenga el nombre correcto de la provincia y ten en cuenta que las provincias del Perú son: ' +
            ", ".join(provincias_validas)},
        {"role": "user", "content": prompt}
    ]

    # Generar la respuesta usando el modelo GPT
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Modelo más económico y con mejor capacidad
        messages=mensajes
    )

    # Obtener la respuesta del asistente
    assistant_response = completion.choices[0].message.content.strip()

    # Validar la respuesta
    if assistant_response in provincias_validas:
        return assistant_response

        # Intentar corregir nombres con similitudes
    close_matches = get_close_matches(
        provincia_normalizada, provincias_validas, n=1, cutoff=0.6)

    # Agregar un manejo específico para términos conocidos que deben corregirse
    terminos_conocidos = {
        "Provincia Constitucional del Callao": "Callao",
        "Cajarca": "Cajamarca",
        "Lia": "Lima",  # Puedes agregar más términos conocidos si es necesario
        "L1M4": "Lima",
        "L1m": "Lima"
    }

    # Si hay coincidencias cercanas, devolver la mejor coincidencia
    if close_matches:
        return close_matches[0]

    if provincia_normalizada in terminos_conocidos:
        return terminos_conocidos[provincia_normalizada]

    return "NA"  # Si la respuesta no es válida, retornar "NA"
