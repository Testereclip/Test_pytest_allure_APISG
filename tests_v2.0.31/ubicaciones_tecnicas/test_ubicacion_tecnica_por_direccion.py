import pytest
import requests
import json
import allure
from pathlib import Path
from config.endpoints import ENDPOINTS


def cargar_direcciones_tecnicas():
    raiz = Path(__file__).resolve().parents[2]
    archivo_json = raiz / 'data' / 'ubicaciones_tecnicas_direcciones.json'
    with archivo_json.open(encoding='utf-8') as f:
        return json.load(f)


@pytest.mark.parametrize("caso", cargar_direcciones_tecnicas())
@allure.feature("Ubicaciones tecnicas")
@allure.story("Ubicaciones Técnicas por Dirección")
@allure.severity(allure.severity_level.CRITICAL)
def test_ubicacion_tecnica_direccion(caso):
    direccion = caso["direccion"]
    esperado = caso["esperado"]

    with allure.step(f"Petición al endpoint con dirección: {direccion}"):
        response = requests.get(
            ENDPOINTS["ubicaciones_tecnicas"],
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
        assert response.status_code == 200, f"Error {response.status_code} al consultar {direccion}"

    with allure.step("Validar estructura del campo 'data'"):
        data = response.json().get("data", {})
        assert isinstance(data, dict), f"'data' no es un objeto en la respuesta para {direccion}"

    with allure.step("Validar atributos esperados en 'data'"):
        for campo, valor_esperado in esperado.items():
            assert campo in data, f"Falta el campo '{campo}' en la respuesta de {direccion}"
            assert data[campo] == valor_esperado, (
                f"Valor incorrecto para '{campo}' en {direccion}: "
                f"esperado '{valor_esperado}', recibido '{data[campo]}'"
            )

        allure.attach(
            json.dumps(data, ensure_ascii=False, indent=2),
            name=f"Datos validados ({direccion})",
            attachment_type=allure.attachment_type.JSON
        )
