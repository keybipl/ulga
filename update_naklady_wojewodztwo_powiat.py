import os
import unicodedata

import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "psi.settings")
django.setup()

from website.models import Gmina


def normalize_string(s):
    """Normalizuje string - usuwa polskie znaki diakrytyczne i konwertuje na małe litery."""
    if not s:
        return ""
    # Normalizacja NFD - rozbija znaki na bazę + diakrytyki
    nfd = unicodedata.normalize("NFD", str(s))
    # Filtruje tylko podstawowe znaki (bez diakrytyki)
    without_diacritics = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    return without_diacritics.lower().strip()


# Wczytaj dane z Excela
file_path = "bezrobocie.xlsx"
print(f"Wczytywanie danych z pliku: {file_path}")

# Wczytaj z header=0 aby pierwsza linijka była nagłówkami
df = pd.read_excel(file_path, header=0)

print(f"Wczytano {len(df)} wierszy")
print(f"Kolumny: {list(df.columns)}")

# Sprawdź pierwsze wiersze
print("\nPierwsze 5 wierszy:")
print(df.head())

updated_count = 0
not_found_count = 0
error_count = 0
not_found_list = []

print("\n" + "=" * 50)

# Iteruj przez wiersze Excela
for idx, row in df.iterrows():
    wojewodztwo = (
        str(row["Województwo"]).strip() if pd.notna(row["Województwo"]) else ""
    )
    powiat = str(row["Powiat"]).strip() if pd.notna(row["Powiat"]) else ""
    min_naklady_mln = row["minimalne nakłady"]

    if not wojewodztwo or not powiat:
        continue

    # Konwertuj z milionów na złotówki
    min_naklady_zl = float(min_naklady_mln) * 1_000_000

    # Normalizuj nazwy dla porównania
    wojewodztwo_normalized = normalize_string(wojewodztwo)
    powiat_normalized = normalize_string(powiat)

    # Znajdź gminy pasujące do województwa i powiatu
    # Próbuj najpierw dokładnego dopasowania
    gminy = Gmina.objects.filter(wojewodztwo__iexact=wojewodztwo, powiat__iexact=powiat)

    # Jeśli nie znaleziono, użyj znormalizowanych wersji
    if not gminy.exists():
        all_gminy = Gmina.objects.all()
        matching_gminy = []

        for gmina in all_gminy:
            gmina_woj_norm = normalize_string(gmina.wojewodztwo)
            gmina_pow_norm = normalize_string(gmina.powiat)

            if (
                gmina_woj_norm == wojewodztwo_normalized
                and gmina_pow_norm == powiat_normalized
            ):
                matching_gminy.append(gmina.id)

        if matching_gminy:
            gminy = Gmina.objects.filter(id__in=matching_gminy)

    if gminy.exists():
        count = gminy.count()
        gminy.update(minimalne_naklady=min_naklady_zl)
        updated_count += count
        print(
            f"✓ Zaktualizowano {count} gmin w {wojewodztwo} / {powiat}: {min_naklady_zl:,.0f} zł"
        )
    else:
        not_found_count += 1
        not_found_list.append(f"{wojewodztwo} / {powiat}")
        print(f"✗ Nie znaleziono gmin dla: {wojewodztwo} / {powiat}")

print("\n" + "=" * 50)
print("PODSUMOWANIE:")
print(f"Zaktualizowano gmin: {updated_count}")
print(f"Nie znaleziono par województwo/powiat: {not_found_count}")
print(f"Błędów: {error_count}")

if not_found_list:
    print("\nPary województwo/powiat nie znalezione w bazie:")
    for item in not_found_list:
        print(f"  - {item}")

print("=" * 50)
