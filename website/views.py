import locale

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Artykul, Gmina
from .forms import KalkulatorPSIForm
from .calculators import PSICalculator

# Ustaw polską lokalizację dla sortowania
locale_set = False
for loc in ["pl_PL.UTF-8", "pl_PL.utf8", "Polish_Poland.1250", "pl_PL"]:
    try:
        locale.setlocale(locale.LC_COLLATE, loc)
        locale_set = True
        break
    except locale.Error:
        continue

# Jeśli nie udało się ustawić polskiego locale, użyj prostego sortowania
if not locale_set:
    # Fallback - prosty key function dla polskich znaków
    def polish_sort_key(text):
        """Sortowanie z uwzględnieniem polskich znaków"""
        replacements = {
            "ą": "a~",
            "ć": "c~",
            "ę": "e~",
            "ł": "l~",
            "ń": "n~",
            "ó": "o~",
            "ś": "s~",
            "ź": "z~",
            "ż": "z~~",
            "Ą": "A~",
            "Ć": "C~",
            "Ę": "E~",
            "Ł": "L~",
            "Ń": "N~",
            "Ó": "O~",
            "Ś": "S~",
            "Ź": "Z~",
            "Ż": "Z~~",
        }
        result = text.lower()
        for pl_char, replacement in replacements.items():
            result = result.replace(pl_char.lower(), replacement)
        return result

    # Nadpisz locale.strxfrm fallbackiem
    locale.strxfrm = polish_sort_key

# Create your views here.


def home(request):
    return render(request, "website/base.html")


def gminy_list(request):
    """Widok z listą wszystkich gmin - teraz z AJAX loading"""
    # Pobierz unikalne województwa dla dropdown
    wojewodztwa_all = Gmina.objects.values_list("wojewodztwo", flat=True)
    wojewodztwa = list(
        set(wojewodztwa_all)
    )  # Użyj set() dla prawdziwych unikalnych wartości

    # Sortuj województwa alfabetycznie z polskimi znakami
    wojewodztwa.sort(key=locale.strxfrm)

    # Statystyki ogólne
    total_count = Gmina.objects.count()

    context = {
        "wojewodztwa": wojewodztwa,
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
    )

    # Usuń duplikaty i sortuj w Pythonie z polskimi znakami
    powiaty_unique = list(set(powiaty))
    powiaty_sorted = sorted(powiaty_unique, key=locale.strxfrm)

    return JsonResponse({"powiaty": powiaty_sorted})


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

    # Pobierz wszystkie gminy bez sortowania w bazie
    gminy_list = list(gminy)

    # Sortuj w Pythonie z polskimi znakami
    gminy_sorted = sorted(
        gminy_list,
        key=lambda g: (
            locale.strxfrm(g.wojewodztwo),
            locale.strxfrm(g.powiat),
            locale.strxfrm(g.nazwa),
        ),
    )

    # Konwertuj do listy słowników
    gminy_data = []
    for gmina in gminy_sorted:
        gminy_data.append(
            {
                "id": gmina.id,
                "nazwa": gmina.nazwa,
                "wojewodztwo": gmina.wojewodztwo,
                "powiat": gmina.powiat,
                "kod_teryt": gmina.kod_teryt,
                "rodzaj": gmina.rodzaj,
                "intensywnosc_pomocy": float(gmina.intensywnosc_pomocy),
                "minimalne_naklady": (
                    float(gmina.minimalne_naklady) if gmina.minimalne_naklady else None
                ),
                "gmina_tracaca": gmina.gmina_tracaca,
                "stopa_bezrobocia": (
                    float(gmina.stopa_bezrobocia) if gmina.stopa_bezrobocia else None
                ),
                "strefa_ekonomiczna": gmina.strefa_ekonomiczna,
                "liczba_kryteriow_jakosciowych": gmina.get_liczba_kryteriow_jakosciowych(),
            }
        )

    return JsonResponse({"gminy": gminy_data})


def o_programie(request):
    """Widok z informacjami o programie PSI"""
    return render(request, "website/o_programie.html")


def artykuly_list(request):
    """Widok z listą artykułów"""
    artykuly = Artykul.objects.filter(opublikowany=True)
    context = {"artykuly": artykuly}
    return render(request, "website/artykuly_list.html", context)


def artykul_detail(request, slug):
    """Widok pojedynczego artykułu"""
    artykul = get_object_or_404(Artykul, slug=slug, opublikowany=True)
    context = {"artykul": artykul}
    return render(request, "website/artykul_detail.html", context)


def polityka_prywatnosci(request):
    """Widok z Polityką Prywatności"""
    return render(request, "website/polityka_prywatnosci.html")


def uslugi_doradcze(request):
    """Widok z usługami doradczymi"""
    return render(request, "website/uslugi_doradcze.html")


def kryteria_ilosciowe(request):
    """Widok z informacjami o kryteriach ilościowych PSI"""
    return render(request, "website/kryteria_ilosciowe.html")


def kryteria_jakosciowe(request):
    """Widok z informacjami o kryteriach jakościowych PSI"""
    return render(request, "website/kryteria_jakosciowe.html")


def kalkulator_psi(request):
    """Widok kalkulatora PSI"""
    wyniki = None

    if request.method == 'POST':
        form = KalkulatorPSIForm(request.POST)
        if form.is_valid():
            # Pobierz dane z formularza
            gmina = form.cleaned_data['gmina']
            wielkosc_firmy = form.cleaned_data['wielkosc_firmy']
            nowy_zaklad = form.cleaned_data['nowy_zaklad']
            wartosc_inwestycji = form.cleaned_data['wartosc_inwestycji']
            tylko_bpo = form.cleaned_data['tylko_bpo']

            # Wykonaj obliczenia
            kalkulator = PSICalculator(
                gmina=gmina,
                wielkosc_firmy=wielkosc_firmy,
                nowy_zaklad=nowy_zaklad,
                wartosc_inwestycji=wartosc_inwestycji,
                tylko_bpo=tylko_bpo
            )

            wyniki = kalkulator.oblicz_wyniki()
    else:
        form = KalkulatorPSIForm()

    context = {
        'form': form,
        'wyniki': wyniki,
    }

    return render(request, 'website/kalkulator_psi.html', context)