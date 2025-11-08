import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psi.settings')
django.setup()

from website.models import Gmina

print('📊 STATYSTYKI GMIN W BAZIE DANYCH PSI\n')
print('='*60)

# Łączna liczba gmin
total = Gmina.objects.count()
print(f'\n🎯 ŁĄCZNA LICZBA GMIN: {total}\n')

print('='*60)
print('\n📈 ROZKŁAD WEDŁUG INTENSYWNOŚCI POMOCY:\n')

# Rozkład według intensywności
intensywnosci = [0, 15, 25, 30, 35, 40, 50]

for int_val in intensywnosci:
    count = Gmina.objects.filter(intensywnosc_pomocy=int_val).count()
    procent = (count / total * 100) if total > 0 else 0
    
    # Wizualizacja słupkowa
    bar = '█' * int(count / 20)
    
    print(f'{int_val:>3}%: {count:>4} gmin ({procent:>5.1f}%) {bar}')

print('\n' + '='*60)
print('\n📍 ROZKŁAD WEDŁUG WOJEWÓDZTW:\n')

# Województwa
wojewodztwa = Gmina.objects.values_list('wojewodztwo', flat=True).distinct().order_by('wojewodztwo')

for woj in wojewodztwa:
    count = Gmina.objects.filter(wojewodztwo=woj).count()
    print(f'{woj:30s}: {count:>4} gmin')

print('\n' + '='*60)
print('\n🏛️ ROZKŁAD WEDŁUG RODZAJU GMINY:\n')

# Rodzaje gmin
rodzaje = {'GM': 'Gmina miejska', 'GW': 'Gmina wiejska', 'GMW': 'Gmina miejsko-wiejska', 'MNP': 'Miasto na prawach powiatu'}

for kod, nazwa in rodzaje.items():
    count = Gmina.objects.filter(rodzaj=kod).count()
    procent = (count / total * 100) if total > 0 else 0
    print(f'{kod:3s} ({nazwa:27s}): {count:>4} gmin ({procent:>5.1f}%)')

print('\n' + '='*60)
print('\n✅ Statystyki wygenerowane pomyślnie!')
print('\n✅ Statystyki wygenerowane pomyślnie!')
