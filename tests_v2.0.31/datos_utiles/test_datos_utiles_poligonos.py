
import pytest
import requests
import json
import allure
from config.endpoints import ENDPOINTS

with open('data/direccion_poligono.json', encoding='utf-8') as f:
    poligono_data = json.load(f)


@pytest.mark.parametrize("caso", poligono_data)
@allure.feature("Datos Útiles")
@allure.story("Validación de polígono itinerario")
@allure.severity(allure.severity_level.CRITICAL)
def test_validar_poligono_itinerario_por_direccion(caso):
    direccion = caso["direccion"]
    esperado = caso["poligono_itinerario"]

    with allure.step(f"Consultar datos útiles con dirección: {direccion}"):
        params = {"direccion": direccion, "v2": "true"}
        response = requests.get(ENDPOINTS["datos_utiles"], params=params)

    with allure.step("Validar status code 200"):
        assert response.status_code == 200, f"Error en {direccion}"

    with allure.step("Parsear respuesta JSON"):
        json_data = response.json()
        allure.attach(
            response.text,
            name=f"Respuesta JSON - {direccion}",
            attachment_type=allure.attachment_type.JSON
        )
        assert "data" in json_data, f"No se encontró 'data' para {direccion}"
        assert isinstance(json_data["data"], dict), f"'data' no es un objeto para {direccion}"

    with allure.step("Validar polígono itinerario esperado"):
        obtenido = json_data["data"].get("poligono_itinerario")
        assert obtenido == esperado, (
            f"Para '{direccion}' se esperaba '{esperado}' pero se obtuvo '{obtenido}'"
        )
