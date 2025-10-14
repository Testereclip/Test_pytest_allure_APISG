import pytest
import requests
import json
import allure
from config.endpoints import ENDPOINTS

# Cargar datos desde JSON
with open("data/coordenadas_transformar.json", encoding="utf-8") as f:
    test_data = json.load(f)


@allure.feature("Coordenadas - Transformar")
@allure.story("Casos válidos")
@pytest.mark.parametrize("case", test_data["validos"])
def test_coordenadas_validas(case):
    """Validar transformación de coordenadas GKBA → WGS84"""
    with allure.step("Enviar request con coordenadas válidas"):
        response = requests.get(ENDPOINTS["coordenadas_transformar"], params=case["input"])

    with allure.step("Validar status code 200"):
        assert response.status_code == 200

    with allure.step("Validar datos de respuesta transformada"):
        data = response.json().get("data")
        assert pytest.approx(data["x"], rel=1e-6) == case["expected"]["x"]
        assert pytest.approx(data["y"], rel=1e-6) == case["expected"]["y"]


@allure.feature("Coordenadas - Transformar")
@allure.story("Casos inválidos")
@pytest.mark.parametrize("case", test_data["invalidos"])
def test_coordenadas_invalidas(case):
    """Validar respuesta con coordenadas inválidas"""
    with allure.step("Enviar request con coordenadas inválidas"):
        response = requests.get(ENDPOINTS["coordenadas_transformar"], params=case["input"])

    with allure.step(f"Validar status code {case['status_code']}"):
        assert response.status_code == case["status_code"]
