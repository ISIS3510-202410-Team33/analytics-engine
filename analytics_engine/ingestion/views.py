import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from analytics_engine.settings import FIREBASE_BUCKET as bucket
from processing.views import *


def analytics_top_buildings(request):
    res = ingest_top_buildings(request)
    return process_top_buildings(res)


def ingest_top_buildings(request):
    """
    Ingests the data for the process in question
    :param request: HTTP request
    :return: list of the x top buildings
    """
    # TODO: generic numbering through attribute in request

    try:
        # Diccionario para almacenar los conteos por edificio
        conteos_por_edificio = {}

        # Obtener la lista de objetos en el bucket
        blobs = bucket.list_blobs()

        # Iterar sobre los objetos y procesar cada archivo
        for blob in blobs:
            # Obtener el nombre del archivo
            filename = blob.name

            # Ignorar el archivo "edificios.json"
            if filename in ["edificios.json", "calificaciones.json"]:
                continue

            # Descargar el archivo JSON
            blob_content = blob.download_as_string()
            json_data = json.loads(blob_content)

            # Iterar sobre los conteos en el archivo JSON
            for edificio, conteo in json_data.items():
                # Actualizar el conteo del edificio
                conteos_por_edificio[edificio] = conteos_por_edificio.get(edificio, 0) + conteo

        return JsonResponse({
            "msg": {"conteos_por_edificio": conteos_por_edificio}
        }, status=200, safe=False)

    except:
        return JsonResponse({
            "msg: Error ingesting the request"
        }, status=503)
