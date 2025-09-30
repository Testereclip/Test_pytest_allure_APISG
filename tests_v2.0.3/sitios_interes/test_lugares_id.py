import pytest
import requests
import json
import allure
from pathlib import Path
from config.endpoints import ENDPOINTS

# === Cargar JSON de casos ===
def cargar_casos():
    raiz = Path(__file__).resolve().parents[2]  # sube dos niveles hasta raíz del proyecto
    archivo_json = raiz / "data" / "tipos_sitios_id.json"
    with open(archivo_json, encoding="utf-8") as f:
        return json.load(f)["casos"]

@pytest.mark.parametrize("caso", cargar_casos())
def test_tipos_sitios_interes(caso):
    url = f"{ENDPOINTS['tipos_sitios_id']}{caso['id']}"

    with allure.step(f"Consultando endpoint: {url}"):
        response = requests.get(url)
        data = response.json()

        # Adjuntar la URL y la respuesta en el reporte de Allure
        allure.attach(url, name="URL Consultada", attachment_type=allure.attachment_type.TEXT)
        allure.attach(json.dumps(data, indent=2, ensure_ascii=False),
                      name="Respuesta JSON",
                      attachment_type=allure.attachment_type.JSON)

    # === Validaciones ===
    assert response.status_code == 200, f"Status esperado 200, recibido {response.status_code}"
    assert data["data"]["descripcion"] == caso["descripcion_esperada"], \
        f"Descripcion esperada {caso['descripcion_esperada']}, recibida {data['data']['descripcion']}"
    assert data["data"]["esquema"] == caso["esquema"]
    assert data["data"]["estado"] == caso["estado"]
    assert data["data"]["fuente"] == caso["fuente"]
    assert data["data"]["prioridad"] == caso["prioridad"]
    assert data["data"]["tabla"] == caso["tabla"]
