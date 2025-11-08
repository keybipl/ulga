import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "psi.settings")
django.setup()

from website.models import Gmina

swidnickie = Gmina.objects.filter(powiat__icontains="świdnic").order_by(
    "wojewodztwo", "nazwa"
)
print(f"Znaleziono {swidnickie.count()} gmin ze świdnickim w nazwie\n")

print("Gminy świdnickie pogrupowane po województwach:")
current_woj = None
for g in swidnickie:
    if g.wojewodztwo != current_woj:
        current_woj = g.wojewodztwo
        print(f"\n{current_woj}:")
    print(f"  {g.nazwa} (powiat: {g.powiat}): {g.minimalne_naklady:,.0f} zł")
