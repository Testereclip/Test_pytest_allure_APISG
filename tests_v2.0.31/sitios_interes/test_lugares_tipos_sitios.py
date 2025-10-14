import pytest
import requests
import allure
from config.endpoints import ENDPOINTS

@allure.feature("Lugares - Tipos Sitios de Interés")
@allure.story("Validar estructura y datos del endpoint")
def test_tipos_sitios_interes():
    url = ENDPOINTS["tipos_sitios_interes"]

    with allure.step(f"Realizar request al endpoint: {url}"):
        response = requests.get(url)
        assert response.status_code == 200, f"Status esperado 200, recibido {response.status_code}"

    with allure.step("Validar que la respuesta tenga 'data' como lista"):
        json_data = response.json()
        assert "data" in json_data, "La respuesta no contiene 'data'"
        assert isinstance(json_data["data"], list), "'data' no es una lista"

    with allure.step("Validar estructura de cada objeto en 'data'"):
        for item in json_data["data"]:
            assert "descripcion" in item, "Falta campo 'descripcion'"
            assert "esquema" in item, "Falta campo 'esquema'"
            assert "estado" in item, "Falta campo 'estado'"
            assert isinstance(item["estado"], bool), "'estado' debe ser booleano"
            assert "fuente" in item, "Falta campo 'fuente'"
            assert "id_tipo_sitios" in item, "Falta campo 'id_tipo_sitios'"
            assert isinstance(item["id_tipo_sitios"], int), "'id_tipo_sitios' debe ser entero"
            assert "prioridad" in item, "Falta campo 'prioridad'"
            assert isinstance(item["prioridad"], int), "'prioridad' debe ser entero"
            assert "tabla" in item, "Falta campo 'tabla'"

    with allure.step("Validar datos específicos esperados"):
        descripciones = [item["descripcion"] for item in json_data["data"]]
        assert "Hospital General de Agudos" in descripciones, "No se encontró 'Hospital General de Agudos'"
        assert "Hospital Especializado" in descripciones, "No se encontró 'Hospital Especializado'"
