import pytest
import requests
import json
from pathlib import Path
from config.endpoints import ENDPOINTS
import allure


def cargar_casos():
    raiz_proyecto = Path(__file__).resolve().parents[2]
    carpeta_data = raiz_proyecto / 'data'
    archivo_json = carpeta_data / 'direccion_total_cruces.json'

    casos = []
    with archivo_json.open(encoding='utf-8') as f:
        data = json.load(f)
        for entrada in data:
            casos.append({
                "direccion": entrada["direccion"],
                "nombreCalle_1": entrada["nombreCalle_1"],
                "nombreCalle_2": entrada["nombreCalle_2"], 
                "metodo_geocodificacion": entrada["metodo_geocodificacion"],
                "tipoDireccion": entrada["tipoDireccion"],
                "archivo": archivo_json.name
            })
    return casos

# Lista de direcciones que sabes que fallan (los 83 cruces)
DIRECCIONES_CON_ERRORES = {
    "24 DE NOVIEMBRE Y AUTOPISTA 25 DE MAYO",
    "27 DE FEBRERO AV. Y ESCALADA AV.",
    "3 DE FEBRERO Y USHUAIA PASAJE (PJE. PARTICULAR)",
    "ARAOZ DE LAMADRID, GREGORIO, GRAL. Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "ARATA, PEDRO N. Y RIO CUARTO",
    "ARGENTINA AV. Y DELLEPIANE, LUIS, TTE. GRAL",
    "ARGERICH Y VALLE PJE. PARTICULAR (ALT. ARGERICH 500)",
    "AUTOPISTA 25 DE MAYO Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "AUTOPISTA 25 DE MAYO Y DELLEPIANE, LUIS, TTE. GRAL.",
    "AUTOPISTA BUENOS AIRES - LA PLATA Y AUTOPISTA 25 DE MAYO",
    "AUTOPISTA PERITO MORENO Y AUTOPISTA 25 DE MAYO",
    "AUTOPISTA PERITO MORENO Y CHASCOMUS",
    "AUTOPISTA PRESIDENTE HECTOR J. CAMPORA Y AUTOPISTA 25 DE MAYO",
    "AUTOPISTA PRESIDENTE HECTOR J. CAMPORA Y CASTAÑARES AV.",
    "AÑASCO Y TRELLES, MANUEL R.",
    "BALCARCE Y AUTOPISTA 25 DE MAYO",
    "BARCO CENTENERA DEL Y AUTOPISTA 25 DE MAYO",
    "BASTIDAS, MICAELA Y 8 DE MARZO",
    "BASTIDAS, MICAELA Y GILDA",
    "BRANDSEN Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "BRASIL Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "CAFAYATE Y FRAGATA 25 DE MAYO",
    "CALIFORNIA Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "CALVO, CARLOS Y AUTOPISTA 25 DE MAYO",
    "CASTAÑON Y AUTOPISTA 25 DE MAYO",
    "CASTILLO, RAMON S., PRES. AV. Y CALILEGUA",
    "CAÑONERA AMERICA Y FRAGATA 25 DE MAYO",
    "COLOMBRES Y AUTOPISTA 25 DE MAYO",
    "CONSTITUCION Y AUTOPISTA 25 DE MAYO",
    "CORONEL OSORIO Y PUENTE LACARRA - OLIMPICO RIBERA SUR",
    "DAVILA Y AUTOPISTA 25 DE MAYO",
    "DE LA TORRE, LISANDRO Y FRAGATA 25 DE MAYO",
    "DE LOS NIÑOS Y DICIEMBRE 1986",
    "DEL COMERCIO Y AUTOPISTA 25 DE MAYO",
    "DOBLAS Y AUTOPISTA 25 DE MAYO",
    "ESTADO PLURINACIONAL DE BOLIVIA Y MARCOARTU PASAJE (PJE. PARTICULAR)",
    "FINOCHIETTO ENRIQUE DR. Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "HERRERA Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "HORNOS, GRAL. Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "IRIARTE, GRAL. Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "IRIGOYEN, BERNARDO DE Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "JENNER, EDUARDO, DR. Y AUTOPISTA 25 DE MAYO",
    "JUSTO, JUAN B. AV. Y DIAZ, CESAR, GRAL.",
    "LACARRA AV. Y CASTAÑARES AV.",
    "LIMA Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "MANUEL CASTRO Y CORONEL OSORIO",
    "MANUEL CASTRO Y PUENTE LACARRA - OLIMPICO RIBERA SUR",
    "MIRALLA Y DELLEPIANE, LUIS, TTE. GRAL.",
    "MONTIEL Y DELLEPIANE, LUIS, TTE. GRAL.",
    "NORTE PJE. PARTICULAR (ALTURA SILVIO RUGGERI 2750) Y RUGGIERI, SILVIO L.",
    "OBLIGADO RAFAEL, AV.COSTANERA Y EDISON, TOMAS A. AV.",
    "PASAJE E Y LACARRA AV.",
    "PASAJE E Y LAGUNA",
    "PASAJE E Y MARTINEZ CASTRO",
    "PASEO COLON AV. Y LA RABIDA (N) AV.",
    "PAZ, GRAL. AV. Y DELLEPIANE, LUIS, TTE. GRAL.",
    "PERON, EVA AV. Y ACOSTA, MARIANO",
    "PERU Y AUTOPISTA 25 DE MAYO",
    "PITAGORAS Y DIRECTORIO AV.",
    "PUENTE PUEYRREDON Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "PUMACAHUA Y AUTOPISTA 25 DE MAYO",
    "QUINQUELA MARTIN, BENITO Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "RECUERO, CASIMIRO, TTE. CNEL. Y AUTOPISTA 25 DE MAYO",
    "REMEDIOS Y BILBAO, FRANCISCO",
    "RIGLOS Y AUTOPISTA 25 DE MAYO",
    "RIO CUARTO Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "RIO NEGRO Y DELLEPIANE, LUIS, TTE. GRAL.",
    "ROCA, CNEL. AV. Y PJE (AV. ROCA 5400)",
    "ROOSEVELT FRANKLIN D. AV. Y PACHECO",
    "RUCCI, JOSE IGNACIO Y DELLEPIANE, LUIS, TTE. GRAL."
    "SAENZ PEÑA, LUIS, PRES. Y AUTOPISTA 25 DE MAYO",
    "SAENZ VALIENTE, JUAN PABLO (PJE PART RIVER PLATE) Y FIGUEROA ALCORTA, PRES. AV.",
    "SAENZ VALIENTE, JUAN PABLO Y SAENZ VALIENTE, JUAN PABLO (PJE PART RIVER PLATE)",
    "SAN JOSE DE CALASANZ Y AUTOPISTA 25 DE MAYO",
    "SAN JOSE DE CALASANZ Y AUTOPISTA 25 DE MAYO",
    "SANTA FE AV. Y SCALABRINI ORTIZ, RAUL",
    "SANTIAGO DEL ESTERO Y AUTOPISTA 25 DE MAYO",
    "TACUARI Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "TEJEDOR Y AUTOPISTA 25 DE MAYO",
    "VALLE, ARISTOBULO DEL Y AUTOPISTA 1 SUR PRESIDENTE ARTURO FRONDIZI",
    "VARELA AV. Y BILBAO, FRANCISCO",
    "VIEL Y AUTOPISTA 25 DE MAYO",
    "VIEYTES Y IRIARTE, GRAL."
}

@pytest.mark.parametrize("caso", cargar_casos())
@allure.epic("Validaciones de geocoder")
@allure.feature("Geocoder con cruces totales")
@allure.severity(allure.severity_level.NORMAL)
def test_datos_geocoder_con_atributos(caso):
    direccion = caso["direccion"]
    
    # Si la dirección está en la lista de errores, marca el test como known_issue
    if direccion in DIRECCIONES_CON_ERRORES:
        pytest.current_test.marker = pytest.mark.known_issue

def test_datos_geocoder_con_atributos(caso):
    direccion = caso["direccion"]

    allure.dynamic.title(f"Validar geocoder para '{direccion}'")
    allure.dynamic.parameter("Dirección", direccion)
    allure.dynamic.parameter("Archivo origen", caso["archivo"])

    with allure.step("Ejecutar request al endpoint"):
        response = requests.get(
            ENDPOINTS["geocoder"],
            params={"direccion": direccion, "v2": "true"}
        )
        allure.attach(response.url, name="🔗 Request URL", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="📦 Response JSON", attachment_type=allure.attachment_type.JSON)

    with allure.step("Verificar status code 200"):
        assert response.status_code == 200, f"Error HTTP para {direccion}"

    data = response.json().get("data", {})

    # 👇 Reemplaza los dos pasos anteriores (nombreCalle_1 y nombreCalle_2) por este:
    with allure.step("Validar calles de la intersección (orden no importa)"):
        esperado = {caso["nombreCalle_1"], caso["nombreCalle_2"]}
        obtenido = {data.get("nombreCalle_1"), data.get("nombreCalle_2")}
        assert esperado == obtenido, (
            f"[{direccion}] Calles esperadas: {esperado}, obtenidas: {obtenido}"
        )

    with allure.step("Validar campo metodo_geocodificacion"):
        assert data.get("metodo_geocodificacion") == caso["metodo_geocodificacion"], (
            f"[{direccion}] metodo_geocodificacion esperado: {caso['metodo_geocodificacion']}, obtenido: {data.get('metodo_geocodificacion')}"
        )

    with allure.step("Validar campo tipoDireccion"):
        assert data.get("tipoDireccion") == caso["tipoDireccion"], (
            f"[{direccion}] tipoDireccion esperado: {caso['tipoDireccion']}, obtenido: {data.get('tipoDireccion')}"
        )