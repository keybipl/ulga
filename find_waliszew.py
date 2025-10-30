import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psi.settings')
django.setup()

from website.models import Gmina

# Szukaj Wałiszew
print('Szukam gminy Wałiszew...\n')

wałiszew = Gmina.objects.filter(
    wojewodztwo__icontains='mazowieckie',
    nazwa__icontains='wałis'
)

if wałiszew.exists():
    for g in wałiszew:
        print(f'Znaleziono: {g.nazwa} (powiat: {g.powiat})')
        print(f'Kod TERYT: {g.kod_teryt}')
        print(f'Aktualna intensywność: {g.intensywnosc_pomocy}%')
        
        # Zaktualizuj
        g.intensywnosc_pomocy = 0
        g.save()
        print('✅ Zaktualizowano na 0%')
else:
    print('❌ Nie znaleziono gminy zawierającej "wałis" w nazwie')
    
    # Sprawdź wszystkie gminy z powiatu legionowskiego
    print('\nWszystkie gminy z powiatu legionowskiego:')
    leg = Gmina.objects.filter(
        wojewodztwo__icontains='mazowieckie',
        powiat__icontains='legionowski'
    )
    for g in leg:
        print(f'  - {g.nazwa} (intensywność: {g.intensywnosc_pomocy}%)')
        print(f'  - {g.nazwa} (intensywność: {g.intensywnosc_pomocy}%)')
