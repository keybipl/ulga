import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psi.settings')
django.setup()

from website.models import Gmina

print('🔍 WERYFIKACJA INTENSYWNOŚCI POMOCY\n')
print('='*60)

# Sprawdź kujawsko-pomorskie (powinno być 40%)
kuj_pom = Gmina.objects.filter(wojewodztwo__icontains='kujawsko-pomorskie').first()
if kuj_pom:
    print(f'✅ Kujawsko-pomorskie (przykład: {kuj_pom.nazwa}): {kuj_pom.intensywnosc_pomocy}% {"✓ OK" if kuj_pom.intensywnosc_pomocy == 40 else "✗ BŁĄD - powinno być 40%"}')

# Sprawdź zachodniopomorskie (powinno być 40%)
zach_pom = Gmina.objects.filter(wojewodztwo__icontains='zachodniopomorskie').first()
if zach_pom:
    print(f'✅ Zachodniopomorskie (przykład: {zach_pom.nazwa}): {zach_pom.intensywnosc_pomocy}% {"✓ OK" if zach_pom.intensywnosc_pomocy == 40 else "✗ BŁĄD - powinno być 40%"}')

# Sprawdź pomorskie (powinno być 30%)
pom = Gmina.objects.filter(wojewodztwo__iexact='pomorskie').first()
if pom:
    print(f'✅ Pomorskie (przykład: {pom.nazwa}): {pom.intensywnosc_pomocy}% {"✓ OK" if pom.intensywnosc_pomocy == 30 else "✗ BŁĄD - powinno być 30%"}')

# Sprawdź śląskie (powinno być 30%)
slaskie = Gmina.objects.filter(wojewodztwo__iexact='śląskie').first()
if slaskie:
    print(f'✅ Śląskie (przykład: {slaskie.nazwa}): {slaskie.intensywnosc_pomocy}% {"✓ OK" if slaskie.intensywnosc_pomocy == 30 else "✗ BŁĄD - powinno być 30%"}')

# Sprawdź dolnośląskie (powinno być 25%)
dolnoslaskie = Gmina.objects.filter(wojewodztwo__icontains='dolnośląskie').first()
if dolnoslaskie:
    print(f'✅ Dolnośląskie (przykład: {dolnoslaskie.nazwa}): {dolnoslaskie.intensywnosc_pomocy}% {"✓ OK" if dolnoslaskie.intensywnosc_pomocy == 25 else "✗ BŁĄD - powinno być 25%"}')

# Sprawdź powiat poznański (powinno być 15%)
poznan_pow = Gmina.objects.filter(powiat__icontains='poznański').first()
if poznan_pow:
    print(f'✅ Powiat poznański (przykład: {poznan_pow.nazwa}): {poznan_pow.intensywnosc_pomocy}% {"✓ OK" if poznan_pow.intensywnosc_pomocy == 15 else "✗ BŁĄD - powinno być 15%"}')

# Sprawdź miasto Poznań (powinno być 15%)
poznan_miasto = Gmina.objects.filter(nazwa__icontains='Poznań', rodzaj='MNP').first()
if poznan_miasto:
    print(f'✅ Miasto Poznań: {poznan_miasto.intensywnosc_pomocy}% {"✓ OK" if poznan_miasto.intensywnosc_pomocy == 15 else "✗ BŁĄD - powinno być 15%"}')

print('\n' + '='*60)
print('\n📊 ZESTAWIENIE WEDŁUG INTENSYWNOŚCI:\n')

for intensywnosc in [15, 25, 30, 40, 50]:
    count = Gmina.objects.filter(intensywnosc_pomocy=intensywnosc).count()
    print(f'  {intensywnosc}%: {count} gmin')

print('\n' + '='*60)
print('\n' + '='*60)
