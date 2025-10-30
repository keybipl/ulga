"""
Management command do importu gmin z pliku Excel.

Użycie:
    python manage.py import_gminy sciezka/do/pliku.xlsx

Komenda importuje tylko gminy z prawidłowym rodzajem: GW, GM, GMW, MNP
Pozostałe wiersze są ignorowane.
"""

import pandas as pd
from django.core.management.base import BaseCommand, CommandError

from website.models import Gmina


class Command(BaseCommand):
    help = 'Importuje gminy z pliku Excel. Ignoruje wiersze bez prawidłowego rodzaju (GW, GM, GMW, MNP).'

    def add_arguments(self, parser):
        parser.add_argument(
            'plik_excel',
            type=str,
            help='Ścieżka do pliku Excel z danymi gmin'
        )
        parser.add_argument(
            '--aktualizuj',
            action='store_true',
            help='Aktualizuj istniejące gminy zamiast je pomijać'
        )

    def handle(self, *args, **options):
        plik_excel = options['plik_excel']
        aktualizuj = options['aktualizuj']

        # Prawidłowe rodzaje gmin
        DOZWOLONE_RODZAJE = ['GW', 'GM', 'GMW', 'MNP']

        self.stdout.write(self.style.SUCCESS(f'\n📊 Rozpoczynam import z pliku: {plik_excel}\n'))

        # Wczytaj Excel
        try:
            df = pd.read_excel(plik_excel)
        except FileNotFoundError:
            raise CommandError(f'❌ Plik nie został znaleziony: {plik_excel}')
        except Exception as e:
            raise CommandError(f'❌ Błąd podczas wczytywania pliku: {str(e)}')

        # Sprawdź czy są wymagane kolumny
        wymagane_kolumny = [
            'kod_teryt', 'nazwa', 'rodzaj', 'powiat', 'wojewodztwo',
            'intensywnosc_pomocy', 'minimalne_naklady'
        ]
        brakujace = [kol for kol in wymagane_kolumny if kol not in df.columns]
        
        if brakujace:
            raise CommandError(
                f'❌ Brakujące kolumny w pliku Excel: {", ".join(brakujace)}\n'
                f'Dostępne kolumny: {", ".join(df.columns.tolist())}'
            )

        # Opcjonalna kolumna
        if 'gmina_tracaca' not in df.columns:
            df['gmina_tracaca'] = False

        self.stdout.write(f'📋 Znaleziono {len(df)} wierszy w pliku\n')

        # Filtruj tylko gminy z prawidłowym rodzajem
        df_filtrowane = df[df['rodzaj'].isin(DOZWOLONE_RODZAJE)].copy()
        
        ignorowane = len(df) - len(df_filtrowane)
        if ignorowane > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  Zignorowano {ignorowane} wierszy z nieprawidłowym rodzajem gminy'
                )
            )

        self.stdout.write(f'✅ Do importu: {len(df_filtrowane)} gmin\n')

        # Liczniki
        dodane = 0
        zaktualizowane = 0
        pominiete = 0
        bledy = 0

        # Import każdej gminy
        for index, row in df_filtrowane.iterrows():
            try:
                # Przygotuj dane
                kod_teryt = str(row['kod_teryt']).strip()
                
                # Konwersja gmina_tracaca na boolean
                gmina_tracaca = row.get('gmina_tracaca', False)
                if isinstance(gmina_tracaca, str):
                    gmina_tracaca = gmina_tracaca.lower() in ['true', 'tak', '1', 'yes']
                elif pd.isna(gmina_tracaca):
                    gmina_tracaca = False

                dane_gminy = {
                    'nazwa': str(row['nazwa']).strip(),
                    'rodzaj': str(row['rodzaj']).strip().upper(),
                    'powiat': str(row['powiat']).strip(),
                    'wojewodztwo': str(row['wojewodztwo']).strip(),
                    'intensywnosc_pomocy': float(row['intensywnosc_pomocy']),
                    'minimalne_naklady': float(row['minimalne_naklady']),
                    'gmina_tracaca': gmina_tracaca,
                }

                # Sprawdź czy gmina już istnieje
                gmina, created = Gmina.objects.update_or_create(
                    kod_teryt=kod_teryt,
                    defaults=dane_gminy
                )

                if created:
                    dodane += 1
                    self.stdout.write(f'  ✅ Dodano: {gmina.nazwa} ({kod_teryt})')
                elif aktualizuj:
                    zaktualizowane += 1
                    self.stdout.write(f'  🔄 Zaktualizowano: {gmina.nazwa} ({kod_teryt})')
                else:
                    pominiete += 1
                    self.stdout.write(
                        self.style.WARNING(f'  ⏭️  Pominięto (już istnieje): {gmina.nazwa} ({kod_teryt})')
                    )

            except Exception as e:
                bledy += 1
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Błąd w wierszu {index + 2}: {str(e)}')
                )

        # Podsumowanie
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('\n📊 PODSUMOWANIE IMPORTU:\n'))
        self.stdout.write(f'  ✅ Dodano nowych gmin: {dodane}')
        self.stdout.write(f'  🔄 Zaktualizowano: {zaktualizowane}')
        self.stdout.write(f'  ⏭️  Pominięto (już istniały): {pominiete}')
        self.stdout.write(f'  🚫 Zignorowano (nieprawidłowy rodzaj): {ignorowane}')
        if bledy > 0:
            self.stdout.write(self.style.ERROR(f'  ❌ Błędy: {bledy}'))
        self.stdout.write('\n' + '='*60 + '\n')

        if bledy == 0:
            self.stdout.write(self.style.SUCCESS('✨ Import zakończony pomyślnie!\n'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Import zakończony z błędami.\n'))
            self.stdout.write(self.style.WARNING('⚠️  Import zakończony z błędami.\n'))
