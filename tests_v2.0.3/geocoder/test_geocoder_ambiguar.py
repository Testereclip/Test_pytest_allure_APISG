import pytest
import requests
from config.endpoints import ENDPOINTS
import allure


def es_respuesta_ambigua(data):
    return isinstance(data, list) and len(data) > 1


@pytest.mark.parametrize("query, debe_ser_ambigua, debe_tener_metodo", [
    ({"direccion": "PERON 3150", "ambiguar": "true", "v2": "true"}, True, True),
    ({"direccion": "PERON 3150", "ambiguar": "true"}, True, False),
    ({"direccion": "PERON 3150", "ambiguar": "true", "v2": "false"}, True, False),
    ({"direccion": "PERON 3150", "ambiguar": "false"}, False, False),
    ({"direccion": "SARMIENTO 2850", "ambiguar": "true", "v2": "true"}, True, True),
    ({"direccion": "SARMIENTO 2850", "ambiguar": "true"}, True, False),
    ({"direccion": "SARMIENTO 2850", "ambiguar": "true", "v2": "false"}, True, False),
    ({"direccion": "SARMIENTO 2850", "ambiguar": "false"}, False, False),
])

@allure.feature("Ambigüedad y método de geocodificación")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Validación de comportamiento del endpoint **/geocoder** con el parámetro `ambiguar`:
- Si `ambiguar=true`: la respuesta debe ser ambigua (más de un resultado).
- Si `ambiguar=false`: la respuesta debe ser única (un dict o lista con 1).
Además:
- Con `v2=true`: cada item debe incluir `metodo_geocodificacion`.
- Sin `v2` o `v2=false`: no debe incluirse.
""")
def test_ambiguedad_y_metodo(query, debe_ser_ambigua, debe_tener_metodo):
    url = ENDPOINTS["geocoder"]

    allure.dynamic.title(f"Validar ambigüedad={query.get('ambiguar')} v2={query.get('v2')} ({query['direccion']})")
    allure.dynamic.parameter("Dirección", query["direccion"])
    allure.dynamic.parameter("Params", query)

    with allure.step("Ejecutar request al endpoint"):
        response = requests.get(url, params={k: str(v) for k, v in query.items()})
        allure.attach(response.url, name="🔗 Request URL", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="📦 Response JSON", attachment_type=allure.attachment_type.JSON)

    with allure.step("Verificar status code 200"):
        assert response.status_code == 200, (
            f"Fallo request con status {response.status_code}: {response.text}"
        )

    json_data = response.json()
    data = json_data.get("data")

    with allure.step("Validar ambigüedad según parámetro"):
        if debe_ser_ambigua:
            assert es_respuesta_ambigua(data), f"❌ Se esperaba ambigüedad, pero data={data}"
        else:
            assert isinstance(data, dict) or (isinstance(data, list) and len(data) <= 1), (
                f"❌ No se esperaba ambigüedad, pero data={data}"
            )

    with allure.step("Validar presencia/ausencia de metodo_geocodificacion"):
        if debe_tener_metodo:
            assert all("metodo_geocodificacion" in item for item in data), (
                f"❌ Falta 'metodo_geocodificacion' en uno o más ítems para {query}"
            )
        else:
            assert all("metodo_geocodificacion" not in item for item in data), (
                f"❌ 'metodo_geocodificacion' no debería estar presente para {query}"
            )
