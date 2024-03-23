import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from analytics_engine.settings import FIREBASE_BUCKET as bucket


# Create your views here.
def process_top_buildings(request):
    """
    Returns the top number of buildings. Answers BQ 5
    :param request: HTTP request
    :return: list of the x top buildings
    """
    try:
        data = request.content
        data_dict = eval(data)

        conteos_por_edificio = data_dict['msg']['conteos_por_edificio']

        # Ordenar los edificios por la cantidad de visitas (valores) en orden descendente
        top_edificios = sorted(conteos_por_edificio.items(), key=lambda x: x[1], reverse=True)

        # Seleccionar los tres primeros edificios del top
        top_3_edificios = top_edificios[:3]

        return JsonResponse({
            "msg": {"edificios": top_3_edificios}
        }, status=200)

    except:
        return JsonResponse({
            "msg: Error processing the request"
        }, status=503)

