# Archiwum skryptów jednorazowych

Ten katalog zawiera skrypty Python, które były używane do jednorazowych operacji na bazie danych podczas wdrażania projektu.

## Skrypty importu danych:
- `update_naklady_wojewodztwo_powiat.py` - Import minimalnych nakładów z pliku Excel (bezrobocie.xlsx)
- `update_intensywnosc.py` - Aktualizacja intensywności pomocy
- `update_mazowieckie.py` - Specjalne zasady dla województwa mazowieckiego

## Skrypty korekt danych:
- `set_warszawa_0_procent.py` - Ustawienie 0% intensywności dla Warszawy
- `set_null_dla_0_procent.py` - Ustawienie NULL dla minimalnych nakładów gdzie intensywność = 0%
- `update_0_procent.py` - Aktualizacja gmin z 0% intensywności
- `update_granica_wschodnia.py` - Ustawienie 10 mln dla gmin na granicy wschodniej

## Skrypty weryfikacji:
- `check_warszawa.py` - Weryfikacja danych dla Warszawy
- `verify_intensywnosc.py` - Weryfikacja poprawności intensywności
- `verify_swidnicki.py` - Weryfikacja powiatu świdnickiego
- `inspect_bezrobocie.py` - Analiza pliku Excel z danymi

## Skrypty napraw:
- `find_waliszew.py` - Wyszukanie błędnej nazwy Waliszew
- `fix_wieliszew.py` - Naprawa nazwy Wieliszew
- `statystyki_gmin.py` - Statystyki bazy danych

**Uwaga:** Te skrypty są archiwalne i nie są już potrzebne do działania aplikacji. Pozostały na wypadek potrzeby przeglądu historii zmian w bazie danych.
