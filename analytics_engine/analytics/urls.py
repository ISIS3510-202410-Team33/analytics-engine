from django.urls import path
from . import views

urlpatterns = [
    # Test
    path("test/", views.prueba_view),
    path("frequent-buildings/", views.top_buildings)
]
