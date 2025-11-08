import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "psi.settings")
django.setup()

from website.models import Gmina

# Ustaw intensywność pomocy na 0% dla Warszawy
warszawa_gminy = Gmina.objects.filter(nazwa__icontains="warszawa")

print(f'Znaleziono {warszawa_gminy.count()} gmin z "warszawa" w nazwie\n')

print("Przed zmianą:")
for g in warszawa_gminy:
    print(
        f"{g.nazwa} ({g.powiat}, {g.wojewodztwo}) - intensywność: {g.intensywnosc_pomocy}%"
    )

# Ustaw intensywność na 0%
warszawa_gminy.update(intensywnosc_pomocy=0)

print("\n" + "=" * 50)
print("Po zmianie:")
warszawa_gminy = Gmina.objects.filter(nazwa__icontains="warszawa")
for g in warszawa_gminy:
    print(
        f"{g.nazwa} ({g.powiat}, {g.wojewodztwo}) - intensywność: {g.intensywnosc_pomocy}%"
    )

print("\n" + "=" * 50)
print(f"Zaktualizowano intensywność pomocy na 0% dla {warszawa_gminy.count()} gmin")
