import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psi.settings')
django.setup()

from website.models import Gmina

print('🔧 Korekta: aktualizacja Wieliszew na 0%\n')

# Zaktualizuj Wieliszew
updated = Gmina.objects.filter(
    wojewodztwo__icontains='mazowieckie',
    powiat__icontains='legionowski',
    nazwa__icontains='Wieliszew'
).update(intensywnosc_pomocy=0)

print(f'✅ Zaktualizowano Wieliszew: {updated} gmin\n')

# Weryfikacja wszystkich gmin z intensywnością 0%
print('📊 Wszystkie gminy mazowieckie z intensywnością 0%:')
gminy_0 = Gmina.objects.filter(
    wojewodztwo__icontains='mazowieckie',
    intensywnosc_pomocy=0
).order_by('powiat', 'nazwa')

count = 0
current_powiat = ''
for g in gminy_0:
    if g.powiat != current_powiat:
        if current_powiat:
            print()
        print(f'\n{g.powiat}:')
        current_powiat = g.powiat
    print(f'  - {g.nazwa}')
    count += 1

print(f'\n{"="*60}')
print(f'Łącznie: {count} gmin z intensywnością 0%')
print(f'{"="*60}')
print(f'{"="*60}')
