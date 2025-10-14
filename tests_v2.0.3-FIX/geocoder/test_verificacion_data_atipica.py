import pytest 
import requests
import json
from pathlib import Path
from config.endpoints import ENDPOINTS
import allure


def cargar_casos():
    """
    Carga los casos desde geocoder_atipicas.json en /data.
    """
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
                "barrioInf": entrada["barrioInf"],       # 👈 agregado
                "nombreCalle_1": entrada["nombreCalle_1"],
                "archivo": archivo_json.name
            })
    return casos


# =============================
# TEST SIN v2
# =============================
@pytest.mark.parametrize("caso", cargar_casos())
@allure.epic("Validaciones de geocoder")
@allure.feature("Datos básicos sin v2")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Validación del endpoint **/geocoder** sin parámetro `v2`.
Se espera que:
- No aparezca `metodo_geocodificacion`
- Los campos `comuna`, `barrio`, `barrioInf` y `nombreCalle_1` coincidan con el archivo JSON.
""")
def test_datos_geocoder_sin_v2(caso):
    direccion = caso["direccion"]

    allure.dynamic.title(f"Validar datos de geocoder (sin v2) para '{direccion}'")
    allure.dynamic.parameter("Dirección", direccion)
    allure.dynamic.parameter("Archivo origen", caso["archivo"])

    with allure.step("Ejecutar request al endpoint"):
        response = requests.get(
            ENDPOINTS["geocoder"],
            params={"direccion": direccion}
        )
        allure.attach(response.url, name="🔗 Request URL", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="📦 Response JSON", attachment_type=allure.attachment_type.JSON)

    with allure.step("Verificar status code 200"):
        assert response.status_code == 200, f"Error HTTP para {direccion}"

    data = response.json().get("data", {})

    with allure.step("Validar que NO aparezca metodo_geocodificacion"):
        assert "metodo_geocodificacion" not in data, (
            f"[{direccion}] No se esperaba 'metodo_geocodificacion', pero se recibió: {data.get('metodo_geocodificacion')}"
        )

    with allure.step("Validar campo comuna"):
        assert data.get("comuna") == caso["comuna"]

    with allure.step("Validar campo barrio"):
        assert data.get("barrio") == caso["barrio"]

    with allure.step("Validar campo barrioInf"):
        assert data.get("barrioInf") == caso["barrioInf"]

    with allure.step("Validar campo nombreCalle_1"):
        assert str(data.get("nombreCalle_1")) == str(caso["nombreCalle_1"])


# =============================
# TEST CON v2=true
# =============================
@pytest.mark.parametrize("caso", cargar_casos())
@allure.epic("Validaciones de geocoder")
@allure.feature("Datos básicos con v2")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Validación del endpoint **/geocoder** con parámetro `v2=true`.
Se espera que:
- Aparezca `metodo_geocodificacion` con valor `"Geocodificación Directa"`
- Los campos `comuna`, `barrio`, `barrioInf` y `nombreCalle_1` coincidan con el archivo JSON.
""")
def test_datos_geocoder_con_v2(caso):
    direccion = caso["direccion"]

    allure.dynamic.title(f"Validar datos de geocoder (con v2) para '{direccion}'")
    allure.dynamic.parameter("Dirección", direccion)
    allure.dynamic.parameter("Archivo origen", caso["archivo"])

    with allure.step("Ejecutar request al endpoint con v2=true"):
        response = requests.get(
            ENDPOINTS["geocoder"],
            params={"direccion": direccion, "v2": "true"}
        )
        allure.attach(response.url, name="🔗 Request URL", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="📦 Response JSON", attachment_type=allure.attachment_type.JSON)

    with allure.step("Verificar status code 200"):
        assert response.status_code == 200, f"Error HTTP para {direccion}"

    data = response.json().get("data", {})

    with allure.step("Validar que aparezca metodo_geocodificacion correcto"):
        assert data.get("metodo_geocodificacion") == "Geocodificación Directa", (
            f"[{direccion}] Se esperaba 'Geocodificación Directa', obtenido: {data.get('metodo_geocodificacion')}"
        )

    with allure.step("Validar campo comuna"):
        assert data.get("comuna") == caso["comuna"]

    with allure.step("Validar campo barrio"):
        assert data.get("barrio") == caso["barrio"]

    with allure.step("Validar campo barrioInf"):
        assert data.get("barrioInf") == caso["barrioInf"]

    with allure.step("Validar campo nombreCalle_1"):
        assert str(data.get("nombreCalle_1")) == str(caso["nombreCalle_1"])
