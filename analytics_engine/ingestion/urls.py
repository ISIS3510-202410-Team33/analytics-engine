from django.urls import path
from . import views

urlpatterns = [
    # Test
    path("frequent-buildings/", views.analytics_top_buildings)
]
