import pytest
import requests
import json
import allure
from config.endpoints import ENDPOINTS

BASE_URL = ENDPOINTS["lugares_reverse"]

# Cargar dataset de errores
with open("data/lugares_reverse_errores.json", encoding="utf-8") as f:
    errores_data = json.load(f)


@pytest.mark.parametrize("case", errores_data)
@allure.feature("Reverse")
@allure.story("Lugares Reverse - Manejo de errores")
@allure.severity(allure.severity_level.CRITICAL)
def test_lugares_reverse_errores(case):
    """
    Validar mensajes de error del endpoint /lugares/reverse
    con datos inválidos, usando dataset JSON externo.
    """
    with allure.step(f"Enviar petición con parámetros inválidos: {case['params']}"):
        r = requests.get(BASE_URL, params=case["params"])
        allure.attach(
            r.text,
            name="Respuesta cruda",
            attachment_type=allure.attachment_type.JSON
        )
        allure.attach(
            json.dumps(case, ensure_ascii=False, indent=2),
            name="Caso esperado",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Validar código de estado HTTP"):
        assert r.status_code == 400, f"Se esperaba 400, se obtuvo {r.status_code}"

    with allure.step("Validar mensaje de error en la respuesta"):
        body = r.json()
        assert "error" in body, f"La respuesta no contiene campo 'error': {body}"
        assert case["expected_msg"] in body["error"], (
            f"Se esperaba '{case['expected_msg']}', se obtuvo '{body['error']}'"
        )
        allure.attach(
            json.dumps(body, ensure_ascii=False, indent=2),
            name="Error validado",
            attachment_type=allure.attachment_type.JSON
        )
