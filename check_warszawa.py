import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "psi.settings")
django.setup()

from website.models import Gmina

# Znajdź Warszawę
warszawa = Gmina.objects.filter(nazwa__icontains="warszawa")

print(f'Znaleziono {warszawa.count()} gmin z "warszawa" w nazwie\n')

for g in warszawa:
    print(f"Gmina: {g.nazwa}")
    print(f"Powiat: {g.powiat}")
    print(f"Województwo: {g.wojewodztwo}")
    print(f"Rodzaj: {g.rodzaj}")
    print(f"Intensywność pomocy: {g.intensywnosc_pomocy}%")
    print(f"Minimalne nakłady: {g.minimalne_naklady:,.0f} zł")
    print("-" * 50)
