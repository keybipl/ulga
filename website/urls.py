from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("gminy/", views.gminy_list, name="gminy_list"),
    path("o-programie/", views.o_programie, name="o_programie"),
    # API endpoints dla AJAX
    path("api/powiaty/", views.api_get_powiaty, name="api_get_powiaty"),
    path("api/gminy/", views.api_get_gminy, name="api_get_gminy"),
]
