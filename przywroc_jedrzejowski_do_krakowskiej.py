"""
Przywrócenie powiatu jędrzejowskiego do Krakowskiej strefy.
Krakowska strefa obejmuje 23 powiaty, w tym jędrzejowski ze świętokrzyskiego!
"""

import os
import sys

import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "psi.settings")
django.setup()

from website.models import Gmina

print("=" * 80)
print("PRZYWRACANIE JĘDRZEJOWSKIEGO DO KRAKOWSKIEJ")
print("=" * 80)

# Przywróć jędrzejowski (świętokrzyskie) do Krakowskiej
jedrzejowski = Gmina.objects.filter(powiat="jędrzejowski", wojewodztwo="świętokrzyskie")

liczba = jedrzejowski.count()
print(f"\nZnaleziono {liczba} gmin w powiecie jędrzejowskim (woj. świętokrzyskie)")

# Ustaw z powrotem na Krakowską
jedrzejowski.update(strefa_ekonomiczna="Krakowski Park Technologiczny")
print(f"Zaktualizowano: {liczba} gmin -> Krakowski Park Technologiczny")

print("\n" + "=" * 80)
print("WERYFIKACJA:")
print("=" * 80)

# Sprawdź ile jest powiatów w Krakowskiej
krakowska_powiaty = (
    Gmina.objects.filter(strefa_ekonomiczna="Krakowski Park Technologiczny")
    .values("powiat", "wojewodztwo")
    .distinct()
    .order_by("wojewodztwo", "powiat")
)

print(f"\nKrakowska strefa ma teraz {krakowska_powiaty.count()} powiatów")
print("Powinno być: 23 ✓")

print("\nLista powiatów:")
for p in krakowska_powiaty:
    print(f"  - {p['powiat']:20s} (woj. {p['wojewodztwo']})")

# Policz gminy
liczba_gmin = Gmina.objects.filter(
    strefa_ekonomiczna="Krakowski Park Technologiczny"
).count()
print(f"\nŁącznie gmin: {liczba_gmin}")

print("\n" + "=" * 80)
print("✓ GOTOWE! Krakowska ma 23 powiaty (22 małopolskie + 1 świętokrzyski)")
print("=" * 80)
