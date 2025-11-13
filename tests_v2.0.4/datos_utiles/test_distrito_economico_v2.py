import pytest
import requests
import allure
from config.endpoints import ENDPOINTS

# Coordenadas con doble distrito económico
coordenadas_con_dos_distritos = [
    {"x": -58.47257809617107, "y": -34.6002874718921},  # datos del ticket APPCALCBA-152
    {"x": -58.472627524809155, "y": -34.600680243527925},
    {"x": -58.47228188984102, "y": -34.60051983677826},
    {"x": 99377.1638345748, "y": 103169.812015763},
    {"x": -58.472174064906426, "y": -34.60106731205862},
    {"x": 99377.1638345748, "y": 103169.812015763},
]


@pytest.mark.parametrize("coord", coordenadas_con_dos_distritos)
@allure.feature("Datos Útiles")
@allure.story("Validación de distrito económico con v2=true")
@allure.severity(allure.severity_level.CRITICAL)
def test_distrito_economico_doble_valor_con_v2(coord):
    with allure.step(f"Consultar datos útiles con coordenadas {coord} y v2=true"):
        response_v2 = requests.get(
            ENDPOINTS["datos_utiles"],
            params={"x": coord["x"], "y": coord["y"], "v2": "true"}
        )

    with allure.step("Validar status code 200"):
        assert response_v2.status_code == 200, f"Error con v2=true en {coord}"

    with allure.step("Parsear respuesta y validar campos obligatorios"):
        data_v2 = response_v2.json().get("data", {})
        allure.attach(
            response_v2.text,
            name=f"Respuesta JSON v2 - {coord}",
            attachment_type=allure.attachment_type.JSON
        )

        distrito = data_v2.get("distrito_economico", "")
        assert distrito, f"No se encontró 'distrito_economico' en respuesta v2=true para {coord}"

        valores = [d.strip() for d in distrito.split(",")]
        assert len(valores) >= 2, (
            f"Se esperaban al menos 2 valores en 'distrito_economico', se obtuvo: '{distrito}'"
        )

        assert "poligono_itinerario" in data_v2, f"Falta 'poligono_itinerario' con v2=true en {coord}"
        assert "circuito_electoral" in data_v2, f"Falta 'circuito_electoral' con v2=true en {coord}"


@pytest.mark.parametrize("coord", coordenadas_con_dos_distritos)
@allure.feature("Datos Útiles")
@allure.story("Validación de ausencia de polígono y circuito sin v2")
@allure.severity(allure.severity_level.NORMAL)
def test_poligono_y_circuito_sin_v2(coord):
    with allure.step(f"Consultar datos útiles con coordenadas {coord} sin v2"):
        response_no_v2 = requests.get(
            ENDPOINTS["datos_utiles"],
            params={"x": coord["x"], "y": coord["y"]}
        )

    with allure.step("Validar status code 200"):
        assert response_no_v2.status_code == 200, f"Error sin v2 en {coord}"

    with allure.step("Validar que no estén polígono ni circuito"):
        data_no_v2 = response_no_v2.json().get("data", {})
        allure.attach(
            response_no_v2.text,
            name=f"Respuesta JSON sin v2 - {coord}",
            attachment_type=allure.attachment_type.JSON
        )

        assert "poligono_itinerario" not in data_no_v2, f"'poligono_itinerario' no debería estar sin v2 en {coord}"
        assert "circuito_electoral" not in data_no_v2, f"'circuito_electoral' no debería estar sin v2 en {coord}"
