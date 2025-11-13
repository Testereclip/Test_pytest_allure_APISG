import pytest
import requests
import allure
from config.endpoints import ENDPOINTS


@allure.feature("Callejero")
@allure.story("Callejero - Respuesta completa")
@allure.severity(allure.severity_level.CRITICAL)
def test_respuesta_completa():
    with allure.step("Realizar petición al endpoint de callejero"):
        response = requests.get(ENDPOINTS["callejero"])  # <- reemplazá con el correcto
        allure.attach(
            str(response.status_code), 
            name="Código de respuesta", 
            attachment_type=allure.attachment_type.TEXT
        )
    
    with allure.step("Validar que la respuesta sea 200 OK"):
        assert response.status_code == 200, "❌ El endpoint no respondió 200 OK"

    with allure.step("Obtener y validar cantidad de registros"):
        data = response.json().get("data", [])
        total = len(data)
        allure.attach(
            str(total),
            name="Cantidad de registros recibidos",
            attachment_type=allure.attachment_type.TEXT
        )
        assert total == 2743, f"❌ Se esperaban 2743 registros pero se recibieron {total}"
