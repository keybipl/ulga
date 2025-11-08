import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "psi.settings")
django.setup()

from website.models import Gmina

# Znajdź gminy z intensywnością 0%
gminy_0_procent = Gmina.objects.filter(intensywnosc_pomocy=0)

print(f"Znaleziono {gminy_0_procent.count()} gmin z intensywnością 0%")
print("\nPrzykłady przed zmianą:")
for g in gminy_0_procent[:5]:
    print(f"{g.nazwa} - minimalne_naklady: {g.minimalne_naklady}")

# Ustaw minimalne_naklady na NULL
count = gminy_0_procent.update(minimalne_naklady=None)

print("\n" + "=" * 50)
print(f"Zaktualizowano {count} gmin - ustawiono minimalne_naklady na NULL")
print("\nPrzykłady po zmianie:")
gminy_0_procent = Gmina.objects.filter(intensywnosc_pomocy=0)
for g in gminy_0_procent[:5]:
    naklady = g.minimalne_naklady if g.minimalne_naklady is not None else "-"
    print(f"{g.nazwa} - minimalne_naklady: {naklady}")
