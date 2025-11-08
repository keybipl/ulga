"""
Naprawa błędów w powiatach przypisanych do Krakowskiej strefy:
1. Poprawienie wielkości liter w nazwach powiatów
2. Usunięcie jędrzejowskiego (woj. świętokrzyskie) - nie należy do małopolskiego
"""

import os
import sys

import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "psi.settings")
django.setup()

from website.models import Gmina

print("=" * 80)
print("NAPRAWA POWIATÓW W KRAKOWSKIEJ STREFIE")
print("=" * 80)

# 1. Popraw powiaty z wielką literą na małą
poprawki_wielkosc = [
    ("Krakowski", "krakowski"),
    ("Limanowski", "limanowski"),
    ("Suski", "suski"),
]

print("\n1. POPRAWIANIE WIELKOŚCI LITER:")
print("-" * 80)

for stara, nowa in poprawki_wielkosc:
    gminy = Gmina.objects.filter(powiat=stara, wojewodztwo="małopolskie")
    liczba = gminy.count()

    if liczba > 0:
        print(f"  {stara} -> {nowa}: {liczba} gmin")
        gminy.update(powiat=nowa)

# 2. Usuń jędrzejowski ze strefy Krakowskiej (to jest woj. świętokrzyskie, nie małopolskie!)
print("\n2. POPRAWIANIE JĘDRZEJOWSKIEGO:")
print("-" * 80)

jedrzejowski_swietokrzyskie = Gmina.objects.filter(
    powiat="jędrzejowski",
    wojewodztwo="świętokrzyskie",
    strefa_ekonomiczna="Krakowski Park Technologiczny",
)

liczba = jedrzejowski_swietokrzyskie.count()
print(f"  Jędrzejowski (woj. świętokrzyskie) ma {liczba} gmin w Krakowskiej")
print("  Ten powiat należy do woj. świętokrzyskiego, NIE małopolskiego!")

# Sprawdź która strefa powinna być
print("\n  Szukam właściwej strefy dla jędrzejowskiego (świętokrzyskie)...")

# Jędrzejowski w świętokrzyskim powinien należeć do Starachowice lub innej strefy
# Sprawdźmy co mają inne powiaty świętokrzyskie
powiaty_swietokrzyskie = (
    Gmina.objects.filter(wojewodztwo="świętokrzyskie")
    .exclude(powiat="jędrzejowski")
    .values("powiat", "strefa_ekonomiczna")
    .distinct()
)

print("\n  Inne powiaty świętokrzyskie mają strefy:")
strefy_counter = {}
for p in powiaty_swietokrzyskie:
    strefa = p["strefa_ekonomiczna"]
    if strefa:
        strefy_counter[strefa] = strefy_counter.get(strefa, 0) + 1

for strefa, liczba in sorted(strefy_counter.items(), key=lambda x: x[1], reverse=True):
    print(f"    {liczba:2d} powiatów - {strefa}")

# Najprawdopodobniej powinna być Starachowice lub Tarnobrzeska
# Ustaw na podstawie najbardziej popularnej strefy w świętokrzyskim
if strefy_counter:
    najczestsza_strefa = max(strefy_counter.items(), key=lambda x: x[1])[0]
    print(f"\n  Ustawiam jędrzejowski na: {najczestsza_strefa}")
    jedrzejowski_swietokrzyskie.update(strefa_ekonomiczna=najczestsza_strefa)
    print(f"  Zaktualizowano: {liczba} gmin")

print("\n" + "=" * 80)
print("WERYFIKACJA:")
print("=" * 80)

# Sprawdź ile teraz jest powiatów w Krakowskiej
krakowska_powiaty = (
    Gmina.objects.filter(strefa_ekonomiczna="Krakowski Park Technologiczny")
    .values("powiat", "wojewodztwo")
    .distinct()
)

print(f"\nKrakowska strefa ma teraz {krakowska_powiaty.count()} powiatów")
print("Powinno być: 23")

# Sprawdź czy wszystkie są z małopolskiego
spoza_malopolskiego = [
    p for p in krakowska_powiaty if p["wojewodztwo"] != "małopolskie"
]
if spoza_malopolskiego:
    print("\nUWAGA! Powiaty spoza małopolskiego:")
    for p in spoza_malopolskiego:
        print(f"  - {p['powiat']} (woj. {p['wojewodztwo']})")
else:
    print("\n✓ Wszystkie powiaty są z województwa małopolskiego")

print("\n" + "=" * 80)
print("GOTOWE!")
print("=" * 80)
