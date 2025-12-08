from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("gminy/", views.gminy_list, name="gminy_list"),
    path("kalkulator-psi/", views.kalkulator_psi, name="kalkulator_psi"),
    path("o-programie/", views.o_programie, name="o_programie"),
    path("kryteria-ilosciowe/", views.kryteria_ilosciowe, name="kryteria_ilosciowe"),
    path("kryteria-jakosciowe/", views.kryteria_jakosciowe, name="kryteria_jakosciowe"),
    path("artykuly/", views.artykuly_list, name="artykuly_list"),
    path("artykuly/<slug:slug>/", views.artykul_detail, name="artykul_detail"),
    path(
        "polityka-prywatnosci/", views.polityka_prywatnosci, name="polityka_prywatnosci"
    ),
    path("uslugi-doradcze/", views.uslugi_doradcze, name="uslugi_doradcze"),
    # API endpoints dla AJAX
    path("api/powiaty/", views.api_get_powiaty, name="api_get_powiaty"),
    path("api/gminy/", views.api_get_gminy, name="api_get_gminy"),
]
