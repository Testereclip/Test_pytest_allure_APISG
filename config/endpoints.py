BASE_URL = "https://api-serviciosgeo-dev.gcba.gob.ar"

ENDPOINTS = {
    "datos_utiles": f"{BASE_URL}/datos/datos-utiles",
    "adyacentes": f"{BASE_URL}/direcciones/obtener_calles_adyacentes",
    "geocoder": f"{BASE_URL}/direcciones/geocoder",
    "ubicaciones_tecnicas": f"{BASE_URL}/ubicaciones/tecnica",
    "calles_nombre": f"{BASE_URL}/calles/nombre",
    "callejero": f"{BASE_URL}/obtener_callejero",
    "reverse": f"{BASE_URL}/coordenadas/reverse",
    "lugares_sugerencias": f"{BASE_URL}/lugares/sugerencias",
    "lugares_busqueda": f"{BASE_URL}/lugares/busqueda",
    "tipos_sitios_interes": f"{BASE_URL}/lugares/tipos-sitios-interes",
    "prioridades": f"{BASE_URL}/lugares/prioridades",
    "tipos_sitios_id": f"{BASE_URL}/lugares/tipos-sitios-interes/",
    "lugares_reverse": f"{BASE_URL}/lugares/reverse",
    "lugares_get_object_content": f"{BASE_URL}/lugares/getObjectContent",
    "coordenadas_transformar": f"{BASE_URL}/coordenadas/transformar"
}
