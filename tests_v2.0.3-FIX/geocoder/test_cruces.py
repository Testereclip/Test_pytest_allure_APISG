import pytest
import requests
import json
from pathlib import Path
from config.endpoints import ENDPOINTS
import allure


def cargar_casos():
    raiz_proyecto = Path(__file__).resolve().parents[2]
    carpeta_data = raiz_proyecto / 'data'
    archivo_json = carpeta_data / 'direccion_cruces_abyba.json'

    casos = []
    with archivo_json.open(encoding='utf-8') as f:
        data = json.load(f)
        for entrada in data:
            casos.append({
                "direccion": entrada["direccion"],
                "nombreCalle_1": entrada["nombreCalle_1"],
                "nombreCalle_2": entrada["nombreCalle_2"], 
                "metodo_geocodificacion": entrada["metodo_geocodificacion"],
                "tipoDireccion": entrada["tipoDireccion"],
                "archivo": archivo_json.name
            })
    return casos


@pytest.mark.parametrize("caso", cargar_casos())
@allure.epic("Validaciones de geocoder")
@allure.feature("Geocoder con cruces ab y ba ")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
Validación del endpoint **/geocoder** verificando que los atributos
`direccion`, `nombreCalle_1`, `nombreCalle_2`, `metodo_geocodificacion` y `tipoDireccion`
coincidan con lo definido en el archivo JSON.
""")
def test_datos_geocoder_con_atributos(caso):
    direccion = caso["direccion"]

    allure.dynamic.title(f"Validar geocoder para '{direccion}'")
    allure.dynamic.parameter("Dirección", direccion)
    allure.dynamic.parameter("Archivo origen", caso["archivo"])

    with allure.step("Ejecutar request al endpoint"):
        response = requests.get(
            ENDPOINTS["geocoder"],
            params={"direccion": direccion, "v2": "true"}
        )
        allure.attach(response.url, name="🔗 Request URL", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="📦 Response JSON", attachment_type=allure.attachment_type.JSON)

    with allure.step("Verificar status code 200"):
        assert response.status_code == 200, f"Error HTTP para {direccion}"

    data = response.json().get("data", {})

    # 👇 Reemplaza los dos pasos anteriores (nombreCalle_1 y nombreCalle_2) por este:
    with allure.step("Validar calles de la intersección (orden no importa)"):
        esperado = {caso["nombreCalle_1"], caso["nombreCalle_2"]}
        obtenido = {data.get("nombreCalle_1"), data.get("nombreCalle_2")}
        assert esperado == obtenido, (
            f"[{direccion}] Calles esperadas: {esperado}, obtenidas: {obtenido}"
        )

    with allure.step("Validar campo metodo_geocodificacion"):
        assert data.get("metodo_geocodificacion") == caso["metodo_geocodificacion"], (
            f"[{direccion}] metodo_geocodificacion esperado: {caso['metodo_geocodificacion']}, obtenido: {data.get('metodo_geocodificacion')}"
        )

    with allure.step("Validar campo tipoDireccion"):
        assert data.get("tipoDireccion") == caso["tipoDireccion"], (
            f"[{direccion}] tipoDireccion esperado: {caso['tipoDireccion']}, obtenido: {data.get('tipoDireccion')}"
        )