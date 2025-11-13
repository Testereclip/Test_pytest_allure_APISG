import pytest
import requests
import json
from pathlib import Path
from config.endpoints import ENDPOINTS
import allure


def cargar_direcciones():
    raiz_proyecto = Path(__file__).resolve().parents[2]
    carpeta_data = raiz_proyecto / "data"

    casos = []
    for archivo in carpeta_data.glob("metodo_*.json"):
        with archivo.open(encoding="utf-8") as f:
            data = json.load(f)
            for entrada in data:
                casos.append({
                    "direccion": entrada["direccion"],
                    "metodo_esperado": entrada["metodo_geocodificacion"],
                    "archivo": archivo.name
                })
    return casos


@pytest.mark.parametrize("caso", cargar_direcciones())
@allure.epic("Validaciones de geocoder")
@allure.feature("Método de geocodificación")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
Validación de que el campo `metodo_geocodificacion` se comporte correctamente
según el parámetro `v2`:
- **v2=true**: debe estar presente y con el valor esperado.
- **sin v2 o v2=false**: no debe aparecer.
""")
def test_metodo_geocodificacion(caso):
    direccion = caso["direccion"]
    metodo_esperado = caso["metodo_esperado"]

    allure.dynamic.title(f"Validar metodo_geocodificacion para '{direccion}'")
    allure.dynamic.parameter("Dirección", direccion)
    allure.dynamic.parameter("Método esperado", metodo_esperado)
    allure.dynamic.parameter("Archivo origen", caso["archivo"])

    # ---------- 1. v2=true ----------
    with allure.step("[v2=true] Ejecutar request"):
        response_v2_true = requests.get(
            ENDPOINTS["geocoder"],
            params={"direccion": direccion, "v2": "true"}
        )
        assert response_v2_true.status_code == 200, f"[v2=true] Error en request para {direccion}"

    with allure.step("[v2=true] Validar metodo_geocodificacion presente y correcto"):
        data_v2_true = response_v2_true.json().get("data", {})
        metodo_obtenido = data_v2_true.get("metodo_geocodificacion")

        assert metodo_obtenido == metodo_esperado, (
            f"[v2=true] Archivo: {caso['archivo']} - Dirección: {direccion} "
            f"- Esperado: {metodo_esperado}, Obtenido: {metodo_obtenido}"
        )

    # ---------- 2. sin v2 ----------
    with allure.step("[sin v2] Ejecutar request"):
        response_sin_v2 = requests.get(
            ENDPOINTS["geocoder"],
            params={"direccion": direccion}
        )
        assert response_sin_v2.status_code == 200, f"[sin v2] Error en request para {direccion}"

    with allure.step("[sin v2] Validar que NO aparezca metodo_geocodificacion"):
        data_sin_v2 = response_sin_v2.json().get("data", {})
        assert "metodo_geocodificacion" not in data_sin_v2, (
            f"[sin v2] Archivo: {caso['archivo']} - Dirección: {direccion} "
            f"- NO se esperaba 'metodo_geocodificacion', pero se recibió: {data_sin_v2.get('metodo_geocodificacion')}"
        )

    # ---------- 3. v2=false ----------
    with allure.step("[v2=false] Ejecutar request"):
        response_v2_false = requests.get(
            ENDPOINTS["geocoder"],
            params={"direccion": direccion, "v2": "false"}
        )
        assert response_v2_false.status_code == 200, f"[v2=false] Error en request para {direccion}"

    with allure.step("[v2=false] Validar que NO aparezca metodo_geocodificacion"):
        data_v2_false = response_v2_false.json().get("data", {})
        assert "metodo_geocodificacion" not in data_v2_false, (
            f"[v2=false] Archivo: {caso['archivo']} - Dirección: {direccion} "
            f"- NO se esperaba 'metodo_geocodificacion', pero se recibió: {data_v2_false.get('metodo_geocodificacion')}"
        )
