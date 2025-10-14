import pytest
import requests
import json
import allure
from config.endpoints import ENDPOINTS


# Lista de direcciones para validar la diferencia de atributos
direcciones_para_test = [
    "1 DE AGOSTO DIA DE LA PACHAMAMA 3902",  # chapas no validas
    "AGÜERO 600",  # chapas no validas
    "MUÑIZ 1250",  # chapas no validas
    "TEGUCIGALPA 1411",  # chapas no validas
    "PI Y MARGALL 750",  # chapas no validas
    "CORRIENTES Y CALLAO",  # interseccion
    "PERU 1050",
    "PICO 4569"
]

# Lista de coordenadas para testear
coordenadas_para_test = [
    {"x": -58.48361576400453, "y": -34.608162159514364},  # WGS84
    {"x": -58.443287510761536, "y": -34.5670284880113},   # WGS84
    {"x": 106809.4329269196, "y": 102045.5880628702},     # GKBA
    {"x": 106822.001113225, "y": 105574.109734017},       # GKBA duplicado
    {"x": -58.48683519023046, "y": -34.57409433025092},   # CU duplicado
    {"x": -58.49560212816951, "y": -34.666730271811616},  # CU duplicado
    {"x": -58.49605838416304, "y": -34.66635617982816}    # CU duplicado
]


@allure.feature("Datos Útiles")
@allure.story("Comparación de atributos por coordenadas con y sin v2")
@pytest.mark.parametrize("coord", coordenadas_para_test)
def test_diferencias_de_atributos_v2_por_coordenadas(coord):
    with allure.step(f"Consultar API con v2=true para coordenadas {coord}"):
        response_v2 = requests.get(ENDPOINTS["datos_utiles"], params={"x": coord["x"], "y": coord["y"], "v2": "true"})
        assert response_v2.status_code == 200, f"Error con v2=true en coordenadas {coord}"
        data_v2 = response_v2.json().get("data", {})

    with allure.step(f"Consultar API sin v2 para coordenadas {coord}"):
        response_no_v2 = requests.get(ENDPOINTS["datos_utiles"], params={"x": coord["x"], "y": coord["y"]})
        assert response_no_v2.status_code == 200, f"Error sin v2 en coordenadas {coord}"
        data_no_v2 = response_no_v2.json().get("data", {})

    with allure.step("Comparar diferencias de claves entre respuestas"):
        keys_v2 = set(data_v2.keys())
        keys_no_v2 = set(data_no_v2.keys())
        solo_en_v2 = keys_v2 - keys_no_v2
        solo_en_no_v2 = keys_no_v2 - keys_v2

        allure.attach(str(solo_en_v2), "Claves solo en v2")
        allure.attach(str(solo_en_no_v2), "Claves solo sin v2")

    with allure.step("Validar que v2 incluye nuevos atributos"):
        assert "poligono_itinerario" in data_v2, f"Falta 'poligono_itinerario' con v2=true en {coord}"
        assert "circuito_electoral" in data_v2, f"Falta 'circuito_electoral' con v2=true en {coord}"

    with allure.step("Validar que los atributos extra no estén sin v2"):
        assert "poligono_itinerario" not in data_no_v2, f"'poligono_itinerario' debería faltar sin v2 en {coord}"
        assert "circuito_electoral" not in data_no_v2, f"'circuito_electoral' debería faltar sin v2 en {coord}"


@allure.feature("Datos Útiles")
@allure.story("Comparación de atributos por direcciones con y sin v2")
@pytest.mark.parametrize("direccion", direcciones_para_test)
def test_diferencias_de_atributos_v2(direccion):
    with allure.step(f"Consultar API con v2=true para dirección {direccion}"):
        response_v2 = requests.get(ENDPOINTS["datos_utiles"], params={"direccion": direccion, "v2": "true"})
        assert response_v2.status_code == 200, f"Error con v2=true en {direccion}"
        data_v2 = response_v2.json().get("data", {})

    with allure.step(f"Consultar API sin v2 para dirección {direccion}"):
        response_no_v2 = requests.get(ENDPOINTS["datos_utiles"], params={"direccion": direccion})
        assert response_no_v2.status_code == 200, f"Error sin v2 en {direccion}"
        data_no_v2 = response_no_v2.json().get("data", {})

    with allure.step("Comparar diferencias de claves entre respuestas"):
        keys_v2 = set(data_v2.keys())
        keys_no_v2 = set(data_no_v2.keys())
        solo_en_v2 = keys_v2 - keys_no_v2
        solo_en_no_v2 = keys_no_v2 - keys_v2

        allure.attach(str(solo_en_v2), "Claves solo en v2")
        allure.attach(str(solo_en_no_v2), "Claves solo sin v2")

    with allure.step("Validar que v2 incluye nuevos atributos"):
        assert "poligono_itinerario" in data_v2, f"Falta 'poligono_itinerario' con v2=true en {direccion}"
        assert "circuito_electoral" in data_v2, f"Falta 'circuito_electoral' con v2=true en {direccion}"

    with allure.step("Validar que los atributos extra no estén sin v2"):
        assert "poligono_itinerario" not in data_no_v2, f"'poligono_itinerario' debería faltar sin v2 en {direccion}"
        assert "circuito_electoral" not in data_no_v2, f"'circuito_electoral' debería faltar sin v2 en {direccion}"
