import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psi.settings')
django.setup()

from website.models import Gmina

print('🚀 Rozpoczynam aktualizację intensywności pomocy na 0% dla wybranych powiatów...\n')

# ========================================
# INTENSYWNOŚĆ 0% - wybrane powiaty i gminy mazowieckie
# ========================================

# Definicja powiatów i gmin do aktualizacji
powiaty_gminy_0 = {
    'legionowski': ['Legionowo', 'Jabłonna', 'Nieporęt', 'Wałiszew'],
    'miński': ['Mińsk Mazowiecki', 'Sulejówek', 'Cegłów', 'Dębe Wielkie', 'Halinów', 'Jakubów', 'Stanisławów'],
    'otwocki': ['Józefów', 'Otwock', 'Celestynów', 'Karczew', 'Wiązowna'],
    'wołomiński': ['Kobyłka', 'Marki', 'Ząbki', 'Zielonka', 'Klembów', 'Poświętne', 'Radzymin', 'Wołomin'],
    'grodziski': ['Milanówek', 'Podkowa Leśna'],
    'nowodworski': ['Nowy Dwór Mazowiecki', 'Czosnów', 'Pomiechówek'],
    'piaseczyński': ['Konstancin-Jeziorna', 'Lesznowola', 'Piaseczno'],
    'warszawski zachodni': ['Izabelin', 'Łomianki', 'Ożarów Mazowiecki', 'Stare Babice'],
    'pruszkowski': []  # Wszystkie gminy z powiatu
}

total_count = 0

for powiat, gminy_list in powiaty_gminy_0.items():
    print(f'📍 Powiat {powiat}:')
    
    if gminy_list:
        # Aktualizuj tylko wybrane gminy
        for gmina_nazwa in gminy_list:
            # Spróbuj dokładnego dopasowania
            updated = Gmina.objects.filter(
                wojewodztwo__icontains='mazowieckie',
                powiat__icontains=powiat,
                nazwa__iexact=gmina_nazwa
            ).update(intensywnosc_pomocy=0)
            
            # Jeśli nie znaleziono, spróbuj z icontains
            if updated == 0:
                updated = Gmina.objects.filter(
                    wojewodztwo__icontains='mazowieckie',
                    powiat__icontains=powiat,
                    nazwa__icontains=gmina_nazwa
                ).update(intensywnosc_pomocy=0)
            
            total_count += updated
            if updated > 0:
                print(f'  ✅ {gmina_nazwa}: {updated} gmin')
            else:
                print(f'  ⚠️  {gmina_nazwa}: 0 gmin (nie znaleziono)')
    else:
        # Aktualizuj cały powiat
        updated = Gmina.objects.filter(
            wojewodztwo__icontains='mazowieckie',
            powiat__icontains=powiat
        ).update(intensywnosc_pomocy=0)
        total_count += updated
        print(f'  ✅ Cały powiat: {updated} gmin')
    
    print()

# ========================================
# PODSUMOWANIE
# ========================================
print('='*60)
print('✨ PODSUMOWANIE AKTUALIZACJI:')
print('='*60)
print(f'  🎯 ŁĄCZNIE ZAKTUALIZOWANO NA 0%: {total_count} gmin')
print('='*60)
print('\n✅ Aktualizacja zakończona pomyślnie!')
print('\nℹ️  Te gminy NIE są objęte wsparciem PSI (intensywność 0%)')
print('\nℹ️  Te gminy NIE są objęte wsparciem PSI (intensywność 0%)')
