from django.http import JsonResponse
from django.shortcuts import render

from .models import Gmina

# Create your views here.


def home(request):
    return render(request, "website/base.html")


def gminy_list(request):
    """Widok z listą wszystkich gmin - teraz z AJAX loading"""
    # Pobierz unikalne województwa dla dropdown
    wojewodztwa = (
        Gmina.objects.values_list("wojewodztwo", flat=True)
        .distinct()
        .order_by("wojewodztwo")
    )

    # Statystyki ogólne
    total_count = Gmina.objects.count()

    context = {
        "wojewodztwa": list(wojewodztwa),
        "total_count": total_count,
    }

    return render(request, "website/gminy_list.html", context)


def api_get_powiaty(request):
    """API endpoint - zwraca powiaty dla wybranego województwa"""
    wojewodztwo = request.GET.get("wojewodztwo")
    if not wojewodztwo:
        return JsonResponse({"powiaty": []})

    powiaty = (
        Gmina.objects.filter(wojewodztwo=wojewodztwo)
        .values_list("powiat", flat=True)
        .distinct()
        .order_by("powiat")
    )
    return JsonResponse({"powiaty": list(powiaty)})


def api_get_gminy(request):
    """API endpoint - zwraca gminy dla wybranego województwa/powiatu"""
    wojewodztwo = request.GET.get("wojewodztwo")
    powiat = request.GET.get("powiat")
    search = request.GET.get("search", "").strip()

    gminy = Gmina.objects.all()

    if wojewodztwo:
        gminy = gminy.filter(wojewodztwo=wojewodztwo)

    if powiat:
        gminy = gminy.filter(powiat=powiat)

    if search:
        gminy = gminy.filter(nazwa__icontains=search)

    gminy = gminy.order_by("wojewodztwo", "powiat", "nazwa")

    # Konwertuj do listy słowników
    gminy_data = []
    for gmina in gminy:
        gminy_data.append(
            {
                "id": gmina.id,
                "nazwa": gmina.nazwa,
                "wojewodztwo": gmina.wojewodztwo,
                "powiat": gmina.powiat,
                "rodzaj": gmina.rodzaj,
                "intensywnosc_pomocy": float(gmina.intensywnosc_pomocy),
                "minimalne_naklady": float(gmina.minimalne_naklady)
                if gmina.minimalne_naklady
                else None,
                "gmina_tracaca": gmina.gmina_tracaca,
            }
        )

    return JsonResponse({"gminy": gminy_data})


def o_programie(request):
    """Widok z informacjami o programie PSI"""
    return render(request, "website/o_programie.html")
