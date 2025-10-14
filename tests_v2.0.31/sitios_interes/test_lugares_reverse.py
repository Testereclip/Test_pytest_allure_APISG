import pytest
import requests
import json
import allure
from config.endpoints import ENDPOINTS

# Cargar datos desde JSON (lista de casos)
with open("data/lugares_reverse.json", encoding="utf-8") as f:
    test_data = json.load(f)

BASE_URL = ENDPOINTS["lugares_reverse"]


@pytest.mark.parametrize("case", test_data)
@allure.feature("Reverese")
@allure.story("Lugares Reverse - Búsqueda de sitios")
@allure.severity(allure.severity_level.CRITICAL)
def test_lugares_reverse(case):
    """
    Validar que el endpoint /lugares/reverse devuelva resultados:
    - Si el parámetro 'id' está presente: debe estar en la respuesta.
    - Si no está: debe devolver sitios de interés en general.
    """
    params = {
        "x": case["coordenadas"]["x"],
        "y": case["coordenadas"]["y"],
        "radio": case["radio"]
    }

    if "id" in case:
        params["id"] = case["id"]

    with allure.step(f"Enviar petición con parámetros: {params}"):
        response = requests.get(BASE_URL, params=params)
        allure.attach(
            response.text,
            name="Respuesta cruda",
            attachment_type=allure.attachment_type.JSON
        )
        allure.attach(
            json.dumps(case, ensure_ascii=False, indent=2),
            name="Caso esperado",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Validar status code"):
        assert response.status_code == 200, f"Se esperaba 200, se obtuvo {response.status_code}"

    with allure.step("Validar datos devueltos"):
        data = response.json().get("data", [])

        if "id" in case:
            assert any(item["id"] == case["id"] for item in data), \
                f"No se encontró el sitio con id {case['id']}"
        else:
            assert len(data) > 0, f"No devolvió sitios de interés para {case}"

        allure.attach(
            json.dumps(data, ensure_ascii=False, indent=2),
            name="Datos validados",
            attachment_type=allure.attachment_type.JSON
        )
