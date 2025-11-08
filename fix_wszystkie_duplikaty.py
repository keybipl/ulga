"""
Kompletny skrypt naprawiający wszystkie duplikaty powiatów
na podstawie oznaczenia województw w nawiasach w oryginalnym dokumencie
"""

import os
import sys

import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "psi.settings")
django.setup()

from website.models import Gmina


def main():
    print("=" * 80)
    print("NAPRAWA WSZYSTKICH DUPLIKATÓW POWIATÓW")
    print("=" * 80)

    poprawki = [
        # (powiat, województwo, właściwa strefa)
        ("grodziski", "mazowieckie", "Łódzka Specjalna Strefa Ekonomiczna"),
        (
            "grodziski",
            "wielkopolskie",
            "Kostrzyńsko-Słubicka Specjalna Strefa Ekonomiczna",
        ),
        (
            "krośnieński",
            "lubuskie",
            "Kostrzyńsko-Słubicka Specjalna Strefa Ekonomiczna",
        ),
        (
            "krośnieński",
            "podkarpackie",
            "Specjalna Strefa Ekonomiczna Euro-Park Mielec",
        ),
        ("bielski", "podlaskie", "Suwalska Specjalna Strefa Ekonomiczna"),
        ("bielski", "śląskie", "Katowicka Specjalna Strefa Ekonomiczna"),
        ("ostrowski", "mazowieckie", "Suwalska Specjalna Strefa Ekonomiczna"),
        (
            "ostrowski",
            "wielkopolskie",
            "Kamiennogórska Specjalna Strefa Ekonomiczna Małej Przedsiębiorczości",
        ),
        (
            "tomaszowski",
            "lubelskie",
            "Tarnobrzeska Specjalna Strefa Ekonomiczna EURO-PARK WISŁOSAN",
        ),
        ("tomaszowski", "łódzkie", "Łódzka Specjalna Strefa Ekonomiczna"),
        ("brzeski", "małopolskie", "Krakowski Park Technologiczny"),
        ("brzeski", "opolskie", "Wałbrzyska Specjalna Strefa Ekonomiczna INVEST-PARK"),
        (
            "opolski",
            "lubelskie",
            "Tarnobrzeska Specjalna Strefa Ekonomiczna EURO-PARK WISŁOSAN",
        ),
        ("opolski", "opolskie", "Wałbrzyska Specjalna Strefa Ekonomiczna INVEST-PARK"),
        ("średzki", "dolnośląskie", "Legnicka Specjalna Strefa Ekonomiczna"),
        (
            "średzki",
            "wielkopolskie",
            "Wałbrzyska Specjalna Strefa Ekonomiczna INVEST-PARK",
        ),
        (
            "świdnicki",
            "dolnośląskie",
            "Wałbrzyska Specjalna Strefa Ekonomiczna INVEST-PARK",
        ),
        ("świdnicki", "lubelskie", "Specjalna Strefa Ekonomiczna Euro-Park Mielec"),
        (
            "nowodworski",
            "mazowieckie",
            "Warmińsko-Mazurska Specjalna Strefa Ekonomiczna",
        ),
        ("nowodworski", "pomorskie", "Pomorska Specjalna Strefa Ekonomiczna"),
    ]

    zmiany = 0

    for powiat, wojewodztwo, strefa in poprawki:
        gminy = Gmina.objects.filter(powiat=powiat, wojewodztwo=wojewodztwo)

        if gminy.exists():
            poprzednia = gminy.first().strefa_ekonomiczna
            liczba = gminy.count()

            if poprzednia != strefa:
                print(f"\n{powiat} (woj. {wojewodztwo}): {liczba} gmin")
                print(f"  Poprzednia: {poprzednia}")
                print(f"  Nowa:       {strefa}")

                gminy.update(strefa_ekonomiczna=strefa)
                zmiany += liczba
                print("  ✓ Zaktualizowano")
            else:
                print(
                    f"\n{powiat} (woj. {wojewodztwo}): {liczba} gmin - OK (bez zmian)"
                )

    print("\n" + "=" * 80)
    print("PODSUMOWANIE")
    print("=" * 80)
    print(f"Zaktualizowano: {zmiany} gmin")

    # Weryfikacja końcowa
    print("\n" + "=" * 80)
    print("WERYFIKACJA STREF")
    print("=" * 80)

    from django.db.models import Count

    strefy = (
        Gmina.objects.values("strefa_ekonomiczna")
        .annotate(liczba=Count("id"))
        .order_by("-liczba")
    )

    for s in strefy:
        if s["strefa_ekonomiczna"]:
            print(f"{s['liczba']:4d} - {s['strefa_ekonomiczna']}")

    print("\n" + "=" * 80)
    print("ZAKOŃCZONO")
    print("=" * 80)


if __name__ == "__main__":
    main()
