import pytest
import requests
import json
import allure
from pathlib import Path
from config.endpoints import ENDPOINTS

# === Cargar JSON de casos ===
def cargar_casos():
    raiz = Path(__file__).resolve().parents[2]
    archivo_json = raiz / "data" / "lugares_object_content.json"
    with open(archivo_json, encoding="utf-8") as f:
        return json.load(f)["casos"]

@pytest.mark.parametrize("caso", cargar_casos())
@allure.feature("GetObjtContent")
@allure.story("GetObjtContent debe regresar datos del sitio de interes que se consulta")
@allure.severity(allure.severity_level.NORMAL)
def test_lugares_object_content(caso):
    url = f"{ENDPOINTS['lugares_get_object_content']}?id_objeto={caso['id_objeto']}"

    with allure.step(f"Consultando endpoint: {url}"):
        response = requests.get(url)

        # Adjuntar respuesta cruda siempre
        allure.attach(url, name="URL Consultada", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="Respuesta cruda", attachment_type=allure.attachment_type.TEXT)

        # Manejar casos en que no viene JSON
        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"La respuesta no es JSON válido. Status={response.status_code}, Body={response.text[:200]}")

        allure.attach(json.dumps(data, indent=2, ensure_ascii=False),
                      name="Respuesta JSON",
                      attachment_type=allure.attachment_type.JSON)

    # === Validaciones base ===
    assert response.status_code == 200, f"Status code inesperado: {response.status_code}"
    assert data["status_code"] == 200, f"status_code esperado 200, recibido {data['status_code']}"

    if "descripcion_esperada" in caso:
        with allure.step(f"Validar descripcion_esperada: esperado='{caso['descripcion_esperada']}', "
                         f"obtenido='{data['data'].get('descripcion')}'"):
            assert data["data"]["descripcion"] == caso["descripcion_esperada"], (
                f"[{caso['id_objeto']}] descripcion_esperada: {caso['descripcion_esperada']}, "
                f"obtenido: {data['data'].get('descripcion')}"
            )

    if "fuente" in caso:
        with allure.step(f"Validar fuente: esperado='{caso['fuente']}', obtenido='{data['data'].get('fuente')}'"):
            assert data["data"]["fuente"] == caso["fuente"], (
                f"[{caso['id_objeto']}] fuente esperada: {caso['fuente']}, "
                f"obtenido: {data['data'].get('fuente')}"
            )

    with allure.step(f"Validar id_objeto: esperado='{caso['id_objeto']}', obtenido='{data['data'].get('id_objeto')}'"):
        assert data["data"]["id_objeto"] == caso["id_objeto"], (
            f"id_objeto esperado: {caso['id_objeto']}, obtenido: {data['data'].get('id_objeto')}"
        )

    # === Validación de tipo_sitio ===
    if "tipo_sitio" in caso:
        with allure.step(f"Validar tipo_sitio: esperado='{caso['tipo_sitio']}', "
                         f"obtenido='{data['data'].get('tipo_sitio')}'"):
            assert str(data["data"]["tipo_sitio"]) == str(caso["tipo_sitio"]), (
                f"[{caso['id_objeto']}] tipo_sitio esperado: {caso['tipo_sitio']}, "
                f"obtenido: {data['data'].get('tipo_sitio')}"
            )

    # === Validación de contenido dinámico ===
    if "contenido" in caso:
        contenido_respuesta = {item["nombre_campo"]: item["valor"] for item in data["data"]["contenido"]}
        for campo, valor_esperado in caso["contenido"].items():
            with allure.step(f"Validar contenido.{campo}: esperado='{valor_esperado}', "
                             f"obtenido='{contenido_respuesta.get(campo)}'"):
                assert contenido_respuesta.get(campo) == valor_esperado, (
                    f"[{caso['id_objeto']}] Para campo '{campo}': "
                    f"esperado {valor_esperado}, recibido {contenido_respuesta.get(campo)}"
                )
