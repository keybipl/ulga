from django.core.management.base import BaseCommand
from website.models import Gmina
import pandas as pd
from decimal import Decimal
import os


class Command(BaseCommand):
    help = 'Aktualizuje minimalne_naklady dla gmin z pliku Excel'

    def add_arguments(self, parser):
        parser.add_argument(
            '--plik',
            type=str,
            default='bezrobocie.xlsx',
            help='Ścieżka do pliku Excel z danymi'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Symulacja bez zapisywania zmian'
        )

    def handle(self, *args, **options):
        # Lista wykluczonych powiatów (lowercase dla łatwiejszego porównania)
        EXCLUDED_POWIATY = {
            'augustowski', 'bartoszycki', 'bialski', 'białostocki', 'bieszczadzki',
            'braniewski', 'chełmski', 'gołdapski', 'hajnowski', 'hrubieszowski',
            'jarosławski', 'kętrzyński', 'lubaczowski', 'przemyski', 'sejneński',
            'siemiatycki', 'sokólski', 'suwalski', 'tomaszowski', 'węgorzewski',
            'włodawski', 'suwałki'
        }

        # Wczytaj plik Excel
        excel_path = options['plik']
        if not os.path.exists(excel_path):
            self.stderr.write(f"Błąd: Plik {excel_path} nie istnieje")
            return

        self.stdout.write(f"Wczytywanie danych z {excel_path}...")
        df = pd.read_excel(excel_path)

        # Mapowanie powiat → minimalne nakłady (konwertuj nazwy powiatów na lowercase dla dopasowania)
        powiat_naklady = {}
        for _, row in df.iterrows():
            powiat = row['Powiat']
            naklady = row['minimalne nakłady']

            # Pomiń puste wiersze
            if pd.isna(powiat) or pd.isna(naklady):
                continue

            # Użyj lowercase jako klucza, aby dopasować nazwy powiatów z bazy danych
            # WAŻNE: wartości w Excel są w milionach PLN, więc mnożymy przez 1,000,000
            powiat_naklady[powiat.lower()] = Decimal(str(naklady)) * 1_000_000

        self.stdout.write(f"Wczytano dane dla {len(powiat_naklady)} powiatów")

        # Statystyki
        updated_count = 0
        skipped_tracace = 0
        skipped_excluded = 0
        not_found = 0

        # Pobierz wszystkie gminy
        all_gminy = Gmina.objects.all()
        total_gminy = all_gminy.count()

        self.stdout.write(f"Przetwarzanie {total_gminy} gmin...")

        for gmina in all_gminy:
            # Pomiń gminy tracące funkcje
            if gmina.gmina_tracaca:
                skipped_tracace += 1
                continue

            # Pomiń wykluczone powiaty
            if gmina.powiat.lower() in EXCLUDED_POWIATY:
                skipped_excluded += 1
                continue

            # Znajdź wartość dla powiatu (porównuj lowercase)
            naklady = powiat_naklady.get(gmina.powiat.lower())

            if naklady is None:
                not_found += 1
                self.stdout.write(
                    self.style.WARNING(f"Brak danych dla powiatu: {gmina.powiat} (gmina: {gmina.nazwa})")
                )
                continue

            # Aktualizuj wartość
            if not options['dry_run']:
                gmina.minimalne_naklady = naklady
                gmina.save(update_fields=['minimalne_naklady', 'data_aktualizacji'])

            updated_count += 1

        # Podsumowanie
        self.stdout.write(self.style.SUCCESS(f"\n=== PODSUMOWANIE ==="))
        self.stdout.write(f"Wszystkich gmin: {total_gminy}")
        self.stdout.write(self.style.SUCCESS(f"Zaktualizowane gminy: {updated_count}"))
        self.stdout.write(self.style.WARNING(f"Pominięte (tracące funkcje): {skipped_tracace}"))
        self.stdout.write(self.style.WARNING(f"Pominięte (wykluczone powiaty): {skipped_excluded}"))
        if not_found > 0:
            self.stdout.write(self.style.ERROR(f"Brak danych w Excel: {not_found}"))

        if options['dry_run']:
            self.stdout.write(self.style.WARNING("\n*** DRY RUN - żadne zmiany nie zostały zapisane ***"))
        else:
            self.stdout.write(self.style.SUCCESS("\n*** Aktualizacja zakończona pomyślnie ***"))
