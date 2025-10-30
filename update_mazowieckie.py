import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psi.settings')
django.setup()

from website.models import Gmina

print('🚀 Rozpoczynam aktualizację intensywności pomocy dla woj. mazowieckiego...\n')

# ========================================
# 1. INTENSYWNOŚĆ 50% - wybrane powiaty mazowieckie
# ========================================
print('📍 Aktualizacja 50% - wybrane powiaty mazowieckie:')

powiaty_50_maz = ['garwoliński', 'łosicki', 'siedlecki', 'sokołowski', 'węgrowski']
count_50_powiaty = 0

for powiat in powiaty_50_maz:
    updated = Gmina.objects.filter(
        wojewodztwo__icontains='mazowieckie',
        powiat__icontains=powiat
    ).update(intensywnosc_pomocy=50)
    count_50_powiaty += updated
    print(f'  ✅ Powiat {powiat}: {updated} gmin')

# Miasto Siedlce
siedlce = Gmina.objects.filter(
    wojewodztwo__icontains='mazowieckie',
    nazwa__icontains='Siedlce',
    rodzaj='MNP'
).update(intensywnosc_pomocy=50)
count_50_powiaty += siedlce
print(f'  ✅ Miasto Siedlce: {siedlce} gmin')

print(f'  📊 Razem 50% (powiaty maz.): {count_50_powiaty} gmin\n')

# ========================================
# 2. INTENSYWNOŚĆ 25% - wybrane gminy mazowieckie
# ========================================
print('📍 Aktualizacja 25% - wybrane gminy mazowieckie:')

gminy_25 = [
    'Baranów', 'Błonie', 'Góra Kalwaria', 'Grodzisk Mazowiecki', 
    'Jaktorów', 'Kampinos', 'Leoncin', 'Leszno', 'Nasielsk', 
    'Prażmów', 'Tarczyn', 'Zakroczym', 'Żabia Wola'
]

count_25_gminy = 0
for gmina in gminy_25:
    updated = Gmina.objects.filter(
        wojewodztwo__icontains='mazowieckie',
        nazwa__iexact=gmina
    ).update(intensywnosc_pomocy=25)
    count_25_gminy += updated
    if updated > 0:
        print(f'  ✅ {gmina}: {updated} gmin')
    else:
        print(f'  ⚠️  {gmina}: 0 gmin (nie znaleziono)')

print(f'  📊 Razem 25% (wybrane gminy): {count_25_gminy} gmin\n')

# ========================================
# 3. INTENSYWNOŚĆ 35% - wybrane gminy mazowieckie
# ========================================
print('📍 Aktualizacja 35% - wybrane gminy mazowieckie:')

gminy_35 = [
    'Dąbrówka', 'Dobre', 'Jadów', 'Kałuszyn', 'Kołbiel', 
    'Latowicz', 'Mrozy', 'Osieck', 'Serock', 'Siennica', 
    'Sobienie-Jeziory', 'Strachówka', 'Tłuszcz'
]

count_35_gminy = 0
for gmina in gminy_35:
    updated = Gmina.objects.filter(
        wojewodztwo__icontains='mazowieckie',
        nazwa__iexact=gmina
    ).update(intensywnosc_pomocy=35)
    count_35_gminy += updated
    if updated > 0:
        print(f'  ✅ {gmina}: {updated} gmin')
    else:
        print(f'  ⚠️  {gmina}: 0 gmin (nie znaleziono)')

print(f'  📊 Razem 35% (wybrane gminy): {count_35_gminy} gmin\n')

# ========================================
# PODSUMOWANIE
# ========================================
print('='*60)
print('✨ PODSUMOWANIE AKTUALIZACJI WOJ. MAZOWIECKIEGO:')
print('='*60)
print(f'  50% (wybrane powiaty + Siedlce): {count_50_powiaty} gmin')
print(f'  35% (wybrane gminy):              {count_35_gminy} gmin')
print(f'  25% (wybrane gminy):              {count_25_gminy} gmin')
print('='*60)
print(f'  🎯 ŁĄCZNIE ZAKTUALIZOWANO: {count_50_powiaty + count_35_gminy + count_25_gminy} gmin')
print('='*60)
print('\n✅ Aktualizacja zakończona pomyślnie!')
print('\n✅ Aktualizacja zakończona pomyślnie!')
