import pytest
import requests
import json
import allure
from pathlib import Path
from config.endpoints import ENDPOINTS  # Archivo con la URL base y endpoints


def cargar_casos():
    """
    Carga los casos desde reverse_coordenadas.json en /data.
    """
    raiz_proyecto = Path(__file__).resolve().parents[2]
    carpeta_data = raiz_proyecto / 'data'
    archivo_json = carpeta_data / 'reverse_coordenadas.json'

    casos = []
    with archivo_json.open(encoding="utf-8") as f:
        data = json.load(f)
        for entrada in data:
            casos.append({
                "x": entrada["x"],
                "y": entrada["y"],
                "direccion": entrada.get("direccion"),
                "comuna": entrada.get("comuna"),
                "barrio": entrada.get("barrio"),
                "codcalle": entrada.get("codcalle"),
                "smp": entrada.get("smp"),
                "status_code": entrada.get("status_code", 200),
                "archivo": archivo_json.name
            })
    return casos


@pytest.mark.parametrize("caso", cargar_casos())
@allure.feature("Reverse")
@allure.story("Reverse coordenadas")
@allure.severity(allure.severity_level.CRITICAL)
def test_reverse_coordenadas(caso):
    """
    Verifica que la respuesta del servicio /coordenadas/reverse coincida con los datos del JSON.
    Maneja casos exitosos (200) y casos de error (ej. 500).
    """
    x, y = caso["x"], caso["y"]
    esperado_status = caso["status_code"]

    with allure.step(f"Petición al endpoint reverse con coordenadas ({x}, {y})"):
        response = requests.get(
            ENDPOINTS["reverse"],
            params={"x": x, "y": y}
        )
        allure.attach(
            response.text,
            name="Respuesta cruda",
            attachment_type=allure.attachment_type.JSON
        )
        allure.attach(
            json.dumps(caso, ensure_ascii=False, indent=2),
            name="Caso esperado",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Validar status code"):
        assert response.status_code == esperado_status, (
            f"[({x}, {y})] Se esperaba HTTP {esperado_status}, "
            f"pero se obtuvo {response.status_code}"
        )

    if esperado_status == 200:
        with allure.step("Validar atributos de la respuesta"):
            data = response.json().get("data", {})

            if caso.get("direccion"):
                assert data.get("direccion") == caso["direccion"], (
                    f"[({x}, {y})] Dirección esperada: {caso['direccion']}, obtenida: {data.get('direccion')}"
                )

            if caso.get("comuna"):
                assert data.get("comuna") == caso["comuna"], (
                    f"[({x}, {y})] Comuna esperada: {caso['comuna']}, obtenida: {data.get('comuna')}"
                )

            if caso.get("barrio"):
                assert data.get("barrio") == caso["barrio"], (
                    f"[({x}, {y})] Barrio esperado: {caso['barrio']}, obtenido: {data.get('barrio')}"
                )

            if caso.get("codcalle"):
                assert str(data.get("codcalle")) == str(caso["codcalle"]), (
                    f"[({x}, {y})] codcalle esperado: {caso['codcalle']}, obtenido: {data.get('codcalle')}"
                )

            if caso.get("smp"):
                assert data.get("smp") == caso["smp"], (
                    f"[({x}, {y})] SMP esperado: {caso['smp']}, obtenido: {data.get('smp')}"
                )

            allure.attach(
                json.dumps(data, ensure_ascii=False, indent=2),
                name="Datos validados",
                attachment_type=allure.attachment_type.JSON
            )
    else:
        with allure.step("Validación de error"):
            allure.attach(
                f"✔ Coordenadas ({x}, {y}) devolvieron correctamente {esperado_status}",
                name="Resultado esperado",
                attachment_type=allure.attachment_type.TEXT
            )
