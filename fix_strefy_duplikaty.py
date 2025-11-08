"""
Skrypt naprawiający przypisanie stref dla powiatów występujących w wielu województwach
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
    print("NAPRAWA DUPLIKATÓW POWIATÓW")
    print("=" * 80)

    # grodziski (woj. wielkopolskie) -> Kostrzyńsko-Słubicka
    grodziski_wlkp = Gmina.objects.filter(
        powiat="grodziski", wojewodztwo="wielkopolskie"
    )

    print(f"\ngrodziski (woj. wielkopolskie): {grodziski_wlkp.count()} gmin")
    print(
        f"  Poprzednia strefa: {grodziski_wlkp.first().strefa_ekonomiczna if grodziski_wlkp.exists() else 'brak'}"
    )

    grodziski_wlkp.update(
        strefa_ekonomiczna="Kostrzyńsko-Słubicka Specjalna Strefa Ekonomiczna"
    )
    print("  ✓ Zaktualizowano na: Kostrzyńsko-Słubicka Specjalna Strefa Ekonomiczna")

    # krośnieński (woj. lubuskie) -> Kostrzyńsko-Słubicka
    krosno_lubuskie = Gmina.objects.filter(powiat="krośnieński", wojewodztwo="lubuskie")

    print(f"\nkrośnieński (woj. lubuskie): {krosno_lubuskie.count()} gmin")
    print(
        f"  Poprzednia strefa: {krosno_lubuskie.first().strefa_ekonomiczna if krosno_lubuskie.exists() else 'brak'}"
    )

    krosno_lubuskie.update(
        strefa_ekonomiczna="Kostrzyńsko-Słubicka Specjalna Strefa Ekonomiczna"
    )
    print("  ✓ Zaktualizowano na: Kostrzyńsko-Słubicka Specjalna Strefa Ekonomiczna")

    # Weryfikacja
    print("\n" + "=" * 80)
    print("WERYFIKACJA")
    print("=" * 80)

    kostrzynska = Gmina.objects.filter(
        strefa_ekonomiczna="Kostrzyńsko-Słubicka Specjalna Strefa Ekonomiczna"
    )

    print(f"\nKostrzyńsko-Słubicka SSE: {kostrzynska.count()} gmin")

    if kostrzynska.count() == 238:
        print("✓ Poprawna liczba gmin (238)!")
    else:
        print(f"⚠ Oczekiwano 238, jest {kostrzynska.count()}")

    print("\n" + "=" * 80)
    print("ZAKOŃCZONO")
    print("=" * 80)


if __name__ == "__main__":
    main()
