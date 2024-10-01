import pytest
from unittest.mock import patch, MagicMock
from src.utils.functions.correct_subzone import c_subzone_3, c_subzone_4


@patch('src.utils.functions.correct_subzone.OpenAI')
def test_c_subzone_3(mock_openai):
    """Prueba para la función c_subzone_3 que corrige nombres de departamentos.

    Esta prueba asegura que la función retorne el departamento corregido o "NA" si no puede corregir.

    Args:
        mock_openai: Simulación del cliente OpenAI.
    """
    mock_client = MagicMock()
    mock_openai.return_value = mock_client  # Simulamos el cliente OpenAI.

    mock_client.chat.completions.create.return_value.choices[
        0].message.content.strip.return_value = "Cajamarca"

    result = c_subzone_3("Cajarca")
    # Verificamos que se retorne el departamento corregido.
    assert result == "Cajamarca"


@patch('src.utils.functions.correct_subzone.OpenAI')
def test_c_subzone_4(mock_openai):
    """Prueba para la función c_subzone_4 que corrige nombres de provincias.

    Esta prueba asegura que la función retorne la provincia corregida o "NA" si no puede corregir.

    Args:
        mock_openai: Simulación del cliente OpenAI.
    """
    mock_client = MagicMock()
    mock_openai.return_value = mock_client  # Simulamos el cliente OpenAI.

    mock_client.chat.completions.create.return_value.choices[
        0].message.content.strip.return_value = "Callao"

    result = c_subzone_4("Provincia Constitucional del Callao")
    # Verificamos que se retorne la provincia corregida.
    assert result == "Callao"
