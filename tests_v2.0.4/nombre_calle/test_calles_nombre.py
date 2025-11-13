import pytest
import requests
import json
from config.endpoints import ENDPOINTS
from urllib.parse import quote
import allure

# Cargar dataset de calles dadas de baja
with open("data/calles_dada_de_baja.json", encoding="utf-8") as f:
    calles_data = json.load(f)


@pytest.mark.parametrize("caso", calles_data)
@allure.feature("Calles_nombre")
@allure.story("Calles dadas de baja")
@allure.description("""
Validación para asegurar que las **calles dadas de baja** no aparezcan 
en los resultados de búsqueda con su `cod_calle` correspondiente.
""")
@allure.severity(allure.severity_level.CRITICAL)
def test_calles_dadas_de_baja_cod_calle_no_debe_aparecer(caso):
    calle_baja = caso["calle"]
    cod_calle_baja = caso["cod_calle"]

    allure.dynamic.title(f"Validar calle dada de baja: {calle_baja} (cod_calle={cod_calle_baja})")
    allure.dynamic.parameter("Calle", calle_baja)
    allure.dynamic.parameter("Cod_calle dado de baja", cod_calle_baja)

    with allure.step("Ejecutar request al endpoint"):
        url = f"{ENDPOINTS['calles_nombre']}?calle={quote(calle_baja)}"
        response = requests.get(url)

    with allure.step("Verificar status code 200"):
        assert response.status_code == 200, f"❌ Error al consultar '{calle_baja}'"

    with allure.step("Obtener coincidencias de la respuesta"):
        data = response.json().get("data", {})
        coincidencias = data.get("calles", [])

    with allure.step("Validar que no aparezca con cod_calle dado de baja"):
        for item in coincidencias:
            cod_calle = item.get("cod_calle")
            if cod_calle == cod_calle_baja:
                pytest.fail(
                    f"❌ La calle '{calle_baja}' con cod_calle={cod_calle_baja} aparece en los resultados "
                    f"pero está dada de baja. No debería estar presente con ese código."
                )
