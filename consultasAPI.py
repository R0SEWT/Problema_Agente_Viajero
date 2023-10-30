import requests


# solo soporta ciudades peruanas juas juas , ESP -> & , -> %2C
def get_consulta(ciudades):
    api_key = 'key=AIzaSyDdPe7-u9-MZvdUXSUR2C-jk9lZywsmWuc'
    consulta = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    origenes = 'origins='
    destinos = 'destinations='

    # pondra una & antes de origins y antes de key
    for e in ciudades:
        if e == ciudades[-1]:
            destinos += e + '%2CPE'
            origenes += e + '%2CPE'
        destinos += e + '%2CPE%7C'
        origenes += e + '%2CPE%7C'

    parametros = origenes + '&' + destinos
    consulta += '&' + parametros + '&' + api_key
    return consulta


def get_json(ciudades):
    consulta = get_consulta(ciudades)
    respuesta = requests.get(consulta)
    datos_en_yeison = respuesta.json()

    print(f"Respuesta del API:\n{datos_en_yeison}")
    return datos_en_yeison


def get_matriz_adyacencia(data_json, n):
    matriz = [[0] * n for _ in range(n)]

    i, j = 0, 0
    for i, row in enumerate(data_json["rows"]):
        for j, e in enumerate(row["elements"]):
            aux = e["distance"]["text"]
            if i != j:
                aux2 = aux.removesuffix(' km')
                matriz[i][j] = int(aux2.replace(",", ""))

    print(f'Matriz:\n{matriz}')
    return matriz


def get_matriz_from_google_maps(ciudades, n):
    data_json = get_json(ciudades)
    matriz = get_matriz_adyacencia(data_json, n)
    return matriz








