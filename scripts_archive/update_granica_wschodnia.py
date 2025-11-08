import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "psi.settings")
django.setup()

from website.models import Gmina

# Lista powiatów z granicy wschodniej
powiaty_granica_wschodnia = [
    "augustowski",
    "bartoszycki",
    "bialski",
    "białostocki",
    "bieszczadzki",
    "braniewski",
    "chełmski",
    "gołdapski",
    "hajnowski",
    "hrubieszowski",
    "jarosławski",
    "kętrzyński",
    "lubaczowski",
    "przemyski",
    "sejneński",
    "siemiatycki",
    "sokólski",
    "suwalski",
    "tomaszowski",
    "węgorzewski",
    "włodawski",
]

# Znajdź wszystkie gminy w tych powiatach
gminy_do_aktualizacji = Gmina.objects.filter(powiat__in=powiaty_granica_wschodnia)

# Dodaj miasto Suwałki (powiat = Suwałki, nazwa = Suwałki)
gminy_do_aktualizacji = gminy_do_aktualizacji | Gmina.objects.filter(
    nazwa="Suwałki", powiat="Suwałki"
)

print(f"Znaleziono {gminy_do_aktualizacji.count()} gmin do aktualizacji\n")

# Pokaż przykłady
print("Przykłady gmin przed zmianą:")
for g in gminy_do_aktualizacji[:10]:
    naklady = g.minimalne_naklady if g.minimalne_naklady else "NULL"
    print(f"{g.nazwa} ({g.powiat}) - {naklady}")

# Aktualizuj minimalne nakłady
count = gminy_do_aktualizacji.update(minimalne_naklady=10000000)

print("\n" + "=" * 50)
print(f"Zaktualizowano {count} gmin - ustawiono minimalne_naklady na 10,000,000 zł")

# Pokaż podsumowanie po powiatach
print("\nPodsumowanie po powiatach:")
for powiat in sorted(powiaty_granica_wschodnia):
    count_powiat = Gmina.objects.filter(
        powiat=powiat, minimalne_naklady=10000000
    ).count()
    if count_powiat > 0:
        print(f"  {powiat}: {count_powiat} gmin")

# Sprawdź Suwałki
suwalki_count = Gmina.objects.filter(
    nazwa="Suwałki", powiat="Suwałki", minimalne_naklady=10000000
).count()
if suwalki_count > 0:
    print(f"  Suwałki (miasto): {suwalki_count} gmina")
