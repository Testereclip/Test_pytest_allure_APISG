import pytest
import requests
import json
import allure
from config.endpoints import ENDPOINTS

# Lista de direcciones para probar
direcciones_para_test = [
    "PELLEGRINI CARLOS E 6022",
    "PERON JUAN DOMINGO TTE GENERAL 2378",
    "RAVIGNANI EMILIO Dr 1850",
    "LAMARCA EMILIO 666",
    "OLAVARRIETA DIEGO de 1410",
    "FERNANDEZ DE LA CRUZ F GRAL AV 3494",
    "GARAY JUAN DE AV 2655",
    "PAGOLA Cnel 3963",
    "CATAMARCA 1409",
    "RAVIGNANI EMILIO Dr 1850",
    "GARAY JUAN DE AV 2655",
    "ARAOZ DE LAMADRID GREGORIO GRAL 728",
    "ALBERDI JUAN BAUTISTA AV 7255",
    "PEDRAZA MANUELA 2077",
    "BROWN ALTE AV 1202",
    "CEVALLOS Virrey 157",
    "ARBELETCHE ANIBAL P 980",
    "SEGUI F J ALTE 2456",
    "RIESTRA AV 5917",
    "ARANGUREN JUAN F Dr 326",
    "BEIRO FRANCISCO AV 5330",
    "PACHECO DE MELO JOSE ANDRES 1887",
    "BOCAYUVA QUINTINO 21",
    "CASCO HORACIO Dr 4650",
    "MENDOZA AV 5320",
    "SAENZ PEÑA LUIS PRES 340",
    "CARACAS 2396",
    "CASTILLO CATULO 2632",
    "GOMEZ VALENTIN 2991",
    "MAGARIÑOS CERVANTES A 5186",
    "ARANGUREN JUAN F Dr 3261",
    "CALDERON DE LA BARCA PEDRO 1797",
    "DUMONT SANTOS 4751",
    "DE LA TORRE LISANDRO 161",
    "LOPEZ VICENTE 1844",
    "GARCIA TEODORO 2380",
    "LACROZE FEDERICO AV 2058",
    "CABRERA JOSE A 5510",
    "PERON JUAN DOMINGO TTE GENERAL 3910",
    "CHILAVERT MARTINIANO CORONEL 6394",
    "FERNANDEZ DE LA CRUZ F GRAL AV 6735",
    "CALVO CARLOS 3651",
    "ALSINA ADOLFO 1842",
    "CAPDEVILA ARTURO 1622",
    "AGUERO 2189",   # doble polígono itinerario
    "AGUERO 2192",   # doble polígono itinerario
    "LAPRIDA 1983"   # doble polígono itinerario
]

def get_coords(direccion):
    url = f"https://api-serviciosgeo-dev.gcba.gob.ar/direcciones/geocoder?direccion={direccion}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json().get("data", {})
        return data.get("coordenada_x"), data.get("coordenada_y")
    except Exception as e:
        pytest.fail(f"Error obteniendo coordenadas para {direccion}: {e}")

def get_datos_utiles(query):
    url = f"{ENDPOINTS['datos_utiles']}?{query}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json().get("data", {})
    except Exception as e:
        pytest.fail(f"Error en datos útiles con query '{query}': {e}")


@allure.feature("Datos Útiles")
@allure.story("Comparación dirección vs coordenadas")
@pytest.mark.parametrize("direccion", direcciones_para_test)
def test_datos_utiles_igual_por_direccion_y_coord(direccion):
    allure.dynamic.title(f"Validar Datos Útiles por dirección y coordenadas: {direccion}")

    with allure.step("Obtener coordenadas desde geocoder"):
        x, y = get_coords(direccion)
        allure.attach(str({"x": x, "y": y}), name="Coordenadas", attachment_type=allure.attachment_type.JSON)
        assert x and y, f"Coordenadas no válidas para {direccion}"

    with allure.step("Consultar Datos Útiles por dirección"):
        data_dir = get_datos_utiles(f"direccion={direccion}&v2=true")
        allure.attach(json.dumps(data_dir, indent=2, ensure_ascii=False), 
                      name="Respuesta Datos Útiles (dirección)", 
                      attachment_type=allure.attachment_type.JSON)

    with allure.step("Consultar Datos Útiles por coordenadas"):
        data_coord = get_datos_utiles(f"x={x}&y={y}&v2=true")
        allure.attach(json.dumps(data_coord, indent=2, ensure_ascii=False), 
                      name="Respuesta Datos Útiles (coordenadas)", 
                      attachment_type=allure.attachment_type.JSON)

    with allure.step("Comparar claves entre ambas respuestas"):
        dif_claves = set(data_dir.keys()) ^ set(data_coord.keys())
        assert not dif_claves, f"❌ Diferencia de claves para '{direccion}': {dif_claves}"

    with allure.step("Comparar valores campo a campo"):
        for key in data_dir:
            val1 = data_dir.get(key)
            val2 = data_coord.get(key)
            assert val1 == val2, f"❌ Para '{direccion}', campo '{key}' difiere:\n - dirección: {val1}\n - coord: {val2}"
