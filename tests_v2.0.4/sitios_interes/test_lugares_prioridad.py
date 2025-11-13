import pytest
import requests
import allure
from config.endpoints import ENDPOINTS

@allure.feature("Lugares")
@allure.story("Validar endpoint prioridades")
def test_lugares_prioridades():
    url = ENDPOINTS["prioridades"]

    with allure.step(f"Consultando el endpoint: {url}"):
        response = requests.get(url)
        allure.attach(str(response.url), "URL Consultada")

    with allure.step("Validar status code 200"):
        assert response.status_code == 200, f"Status code inesperado: {response.status_code}"

    data = response.json().get("data", [])

    with allure.step("Validar que 'data' no esté vacío"):
        assert len(data) > 0, "La lista 'data' está vacía"

    with allure.step("Validar estructura de cada objeto en 'data'"):
        for item in data:
            assert "activo" in item, "Falta campo 'activo'"
            assert "descripcion" in item, "Falta campo 'descripcion'"
            assert "esquema" in item, "Falta campo 'esquema'"
            assert "id_tipo_sitios" in item, "Falta campo 'id_tipo_sitios"
            assert "prioridad" in item, "Falta campo 'prioridad'"
            assert "tabla" in item, "Falta campo 'tabla'"
