import pytest
import requests
import json
from pathlib import Path
from config.endpoints import ENDPOINTS
import allure

VERSION_API = "2.0.3"  # 👈 Indicás la versión que estás probando

def cargar_casos():
    raiz_proyecto = Path(__file__).resolve().parents[2]
    carpeta_data = raiz_proyecto / 'data'
    archivo_json = carpeta_data / 'geocoder_atipicas.json'
    casos = []
    with archivo_json.open(encoding='utf-8') as f:
        data = json.load(f)
        for entrada in data:
            casos.append({
                "direccion": entrada["direccion"],
                "comuna": entrada["comuna"],
                "barrio": entrada["barrio"],
                "barrioInf": entrada["barrioInf"],
                "nombreCalle_1": entrada["nombreCalle_1"],
                "archivo": archivo_json.name
            })
    return casos


@pytest.mark.parametrize("caso", cargar_casos())
@allure.epic("Validaciones de geocoder")
@allure.feature("Datos básicos sin v2")
def test_datos_geocoder_sin_v2(caso):
    direccion = caso["direccion"]
    response = requests.get(ENDPOINTS["geocoder"], params={"direccion": direccion})
    data = response.json().get("data", {})

    assert response.status_code == 200, f"Error HTTP para {direccion}"
    assert "metodo_geocodificacion" not in data

    # 👇 Solo validar estos campos si no estás en la versión con errores conocidos
    if VERSION_API != "2.0.3":
        assert data.get("comuna") == caso["comuna"]
        assert data.get("barrio") == caso["barrio"]
        assert data.get("barrioInf") == caso["barrioInf"]
    else:
        pytest.skip(f"Se omiten validaciones de comuna/barrio/barrioInf por bug conocido en {VERSION_API}")

    assert str(data.get("nombreCalle_1")) == str(caso["nombreCalle_1"])


@pytest.mark.parametrize("caso", cargar_casos())
@allure.epic("Validaciones de geocoder")
@allure.feature("Datos básicos con v2")
def test_datos_geocoder_con_v2(caso):
    direccion = caso["direccion"]
    response = requests.get(ENDPOINTS["geocoder"], params={"direccion": direccion, "v2": "true"})
    data = response.json().get("data", {})

    assert response.status_code == 200, f"Error HTTP para {direccion}"
    assert data.get("metodo_geocodificacion") == "Geocodificación Directa"

    if VERSION_API != "2.0.3":
        assert data.get("comuna") == caso["comuna"]
        assert data.get("barrio") == caso["barrio"]
        assert data.get("barrioInf") == caso["barrioInf"]
    else:
        pytest.skip(f"Se omiten validaciones de comuna/barrio/barrioInf por bug conocido en {VERSION_API}")

    assert str(data.get("nombreCalle_1")) == str(caso["nombreCalle_1"])
