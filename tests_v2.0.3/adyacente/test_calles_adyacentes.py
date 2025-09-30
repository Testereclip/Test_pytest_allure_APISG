import pytest
import requests
import json
import allure
from pathlib import Path
from config import endpoints  # importa tu config


def cargar_direcciones():
    raiz_proyecto = Path(__file__).resolve().parents[2]
    ruta_json = raiz_proyecto / 'data' / 'direccion_adyacente.json'
    with ruta_json.open(encoding='utf-8') as f:
        return json.load(f)


@pytest.mark.parametrize("caso", cargar_direcciones())
@allure.feature("Validación de API")
@allure.story("Calles Adyacentes")
@allure.severity(allure.severity_level.CRITICAL)
def test_calles_adyacentes(caso):
    direccion = caso["direccion"]
    esperados = {caso["Esperado 1"], caso["Esperado 2"]}

    with allure.step(f"Petición al endpoint con dirección: {direccion}"):
        response = requests.get(
            endpoints.ENDPOINTS["adyacentes"],
            params={"direccion": direccion}
        )
        allure.attach(
            response.text,
            name=f"Respuesta API ({direccion})",
            attachment_type=allure.attachment_type.JSON
        )
        allure.attach(
            json.dumps(caso, ensure_ascii=False, indent=2),
            name="Caso esperado",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Validar código de estado HTTP"):
        assert response.status_code == 200, f"Error en request para {direccion}"

    with allure.step("Procesar y validar datos recibidos"):
        data = response.json().get("data", [])

        nombres_lista = [item["nombre_oficial"] for item in data]
        nombres_duplicados = set([x for x in nombres_lista if nombres_lista.count(x) > 1])

        # Adjuntar resultados intermedios
        allure.attach(
            json.dumps(nombres_lista, ensure_ascii=False, indent=2),
            name=f"Nombres recibidos ({direccion})",
            attachment_type=allure.attachment_type.JSON
        )
        if nombres_duplicados:
            allure.attach(
                json.dumps(list(nombres_duplicados), ensure_ascii=False, indent=2),
                name=f"Nombres duplicados ({direccion})",
                attachment_type=allure.attachment_type.JSON
            )

        # Validaciones
        assert not nombres_duplicados, f"Duplicados encontrados: {nombres_duplicados}"

        nombres = set(nombres_lista)
        assert nombres == esperados, f"Para '{direccion}', esperado: {esperados}, recibido: {nombres}"
