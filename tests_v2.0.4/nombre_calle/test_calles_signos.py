import pytest
import requests
import json
from config.endpoints import ENDPOINTS
from urllib.parse import quote
import allure

# Cargar JSON con casos (errores y válidos)
with open("data/calle.json", encoding="utf-8") as f:
    casos = json.load(f)


@pytest.mark.parametrize("caso", casos)
@allure.feature("Calles_nombre")
@allure.story("Validacion de distintos escenario validos o invalidos")
@allure.description("""
Casos de prueba que validan la estructura de la respuesta para:
- Calles con altura
- Cruces
- Calles atípicas
- Mensajes de error (alturas inválidas, consultas vacías, menos de 3 caracteres, consultas con signos)
""")
def test_calles(caso):
    calle = caso.get("calle")
    expected_status = caso.get("status_code", 200)

    # Título dinámico en Allure
    allure.dynamic.title(f"Validación de calle: {calle or '⚠️ consulta vacía'}")
    allure.dynamic.parameter("Calle", calle)
    allure.dynamic.parameter("Status esperado", expected_status)

    if expected_status != 200:
        # --- Caso de error esperado ---
        with allure.step("Ejecutar request con error esperado"):
            url = f"{ENDPOINTS['calles_nombre']}?calle={quote(calle or '')}"
            response = requests.get(url)

        with allure.step("Verificar status code de error"):
            assert response.status_code == expected_status, \
                f"❌ Status incorrecto: esperado {expected_status}, recibido {response.status_code}"

        with allure.step("Verificar contenido del error en respuesta"):
            json_resp = response.json()
            expected_error = caso.get("error")

            assert "error" in json_resp, "❌ La respuesta debería contener 'error'"
            assert json_resp["error"] == expected_error, \
                f"❌ Error inesperado: esperado '{expected_error}', recibido '{json_resp['error']}'"

    else:
        # --- Caso válido ---
        with allure.step("Ejecutar request válido"):
            url = f"{ENDPOINTS['calles_nombre']}?calle={quote(calle)}"
            response = requests.get(url)

        with allure.step("Verificar status code 200"):
            assert response.status_code == 200, f"❌ Error al consultar '{calle}'"

        with allure.step("Validar estructura de la respuesta"):
            json_resp = response.json()
            data = json_resp.get("data", {})
            coincidencias = (data.get("calles") or []) + (data.get("calles_atipicas") or [])

            assert coincidencias, f"❌ No se encontraron resultados para '{calle}'"

        with allure.step("Buscar coincidencia por cod_calle si corresponde"):
            candidato = None
            if "cod_calle" in caso:
                for item in coincidencias:
                    if str(item.get("cod_calle")) == str(caso["cod_calle"]):
                        candidato = item
                        break
                assert candidato, f"❌ No se encontró cod_calle={caso['cod_calle']} en resultados para '{calle}'"
            else:
                candidato = coincidencias[0]

        with allure.step("Validar campos esperados"):
            for key, esperado in caso.items():
                if key in ("calle", "status_code", "error"):
                    continue
                obtenido = candidato.get(key)
                assert str(obtenido) == str(esperado), (
                    f"❌ Mismatch en campo '{key}' para '{calle}': "
                    f"esperado={esperado}, obtenido={obtenido}"
                )
