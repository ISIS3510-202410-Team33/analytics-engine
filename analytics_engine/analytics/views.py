import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from analytics_engine.settings import FIREBASE_BUCKET as bucket


# Create your views here.
@csrf_exempt
def prueba_view(request):
    print(type(bucket))
    return HttpResponse('Ok')



def top_buildings(request):
    """
    Returns the top number of buildings. Answers BQ 5
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

        # Ordenar los edificios por la cantidad de visitas (valores) en orden descendente
        top_edificios = sorted(conteos_por_edificio.items(), key=lambda x: x[1], reverse=True)

        # Seleccionar los tres primeros edificios del top
        top_3_edificios = top_edificios[:3]

        return JsonResponse({
            "msg": {"edificios": top_3_edificios}
        }, status=200)
    except:
        return JsonResponse({"msg: Error processing the request"}, status=503)
