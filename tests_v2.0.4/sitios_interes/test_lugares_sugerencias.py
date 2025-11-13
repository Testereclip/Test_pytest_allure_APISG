import pytest
import requests
import json
import allure
from pathlib import Path
from config.endpoints import ENDPOINTS

# Ruta al JSON con los casos de prueba
def cargar_casos():
    raiz = Path(__file__).resolve().parents[2]
    archivo_json = raiz / "data" / "lugares_sugerencias.json"
    with archivo_json.open(encoding="utf-8") as f:
        return json.load(f)

# Atributos obligatorios en cada sitio
ATRIBUTOS_ESPERADOS = [
    "categoria",
    "direccion",
    "id_sitio",
    "id_tipo_sitios",
    "nombre",
    "prioridad",
    "similaridad",
]


@pytest.mark.parametrize("caso", cargar_casos())
@allure.feature("Sugerencias")
@allure.story("Sugerencias- Debe retornar datos de sitios de interes similares a los que se consultan")
@allure.severity(allure.severity_level.CRITICAL)
def test_lugares_sugerencias(caso):
    sitio_interes = caso["sitio_interes"]
    url = ENDPOINTS["lugares_sugerencias"]

    with allure.step(f"Petición al endpoint con sitio_interes='{sitio_interes}'"):
        response = requests.get(url, params={"sitio_interes": sitio_interes})

        allure.attach(
            response.url,
            name="URL Consultada",
            attachment_type=allure.attachment_type.TEXT
        )
        allure.attach(
            response.text,
            name="Respuesta JSON",
            attachment_type=allure.attachment_type.JSON
        )

    # === CASOS NEGATIVOS ===
    if "status_code" in caso:
        with allure.step("Validar respuesta de error"):
            assert response.status_code == caso["status_code"], \
                f"Se esperaba {caso['status_code']} pero se obtuvo {response.status_code}"
            body = response.json()
            assert "error" in body, "La respuesta de error no contiene campo 'error'"
            assert caso["error"] in body["error"], \
                f"El error esperado era '{caso['error']}', se obtuvo '{body['error']}'"

    # === CASOS POSITIVOS ===
    else:
        with allure.step("Validar código de estado HTTP"):
            assert response.status_code == 200, \
                f"Error {response.status_code} al consultar {sitio_interes}"

        with allure.step("Validar estructura de la respuesta"):
            body = response.json()
            assert "data" in body, "La respuesta no contiene 'data'"
            assert "sitios_de_interes" in body["data"], "La respuesta no contiene 'sitios_de_interes'"

            sitios = body["data"]["sitios_de_interes"]
            assert isinstance(sitios, list), "'sitios_de_interes' no es una lista"
            assert len(sitios) > 0, f"No se devolvieron sitios de interés para {sitio_interes}"

        with allure.step("Validar atributos esperados en cada sitio"):
            for sitio in sitios:
                for atributo in ATRIBUTOS_ESPERADOS:
                    assert atributo in sitio, f"Falta el atributo '{atributo}' en la respuesta"
