import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psi.settings')
django.setup()

from website.models import Gmina

print('🚀 Rozpoczynam aktualizację intensywności pomocy...\n')

# ========================================
# 1. INTENSYWNOŚĆ 15% - wybrane powiaty wielkopolskie + Poznań
# ========================================
print('📍 Aktualizacja 15% - wybrane powiaty wielkopolskie + Poznań:')

# Powiaty: obornicki, poznański, szamotulski, średzki, śremski
powiaty_15 = ['obornicki', 'poznański', 'szamotulski', 'średzki', 'śremski']
count_15_powiaty = 0

for powiat in powiaty_15:
    updated = Gmina.objects.filter(powiat__icontains=powiat).update(intensywnosc_pomocy=15)
    count_15_powiaty += updated
    print(f'  ✅ Powiat {powiat}: {updated} gmin')

# Miasto Poznań (MNP)
poznan = Gmina.objects.filter(nazwa__icontains='Poznań', rodzaj='MNP').update(intensywnosc_pomocy=15)
count_15_powiaty += poznan
print(f'  ✅ Miasto Poznań: {poznan} gmin')

print(f'  📊 Razem 15%: {count_15_powiaty} gmin\n')

# ========================================
# 2. INTENSYWNOŚĆ 50% - województwa wschodnie + podregion siedlecki
# ========================================
print('📍 Aktualizacja 50% - województwa wschodnie:')

wojewodztwa_50 = [
    'lubelskie',
    'podkarpackie',
    'podlaskie',
    'świętokrzyskie',
    'warmińsko-mazurskie'
]

count_50 = 0
for woj in wojewodztwa_50:
    updated = Gmina.objects.filter(wojewodztwo__icontains=woj).update(intensywnosc_pomocy=50)
    count_50 += updated
    print(f'  ✅ Woj. {woj}: {updated} gmin')

# TODO: Podregion siedlecki - wymaga dodatkowego pola w modelu lub mapowania powiatów
# Na razie pominięto - do uzupełnienia po zdefiniowaniu powiatów siedleckich

print(f'  📊 Razem 50%: {count_50} gmin\n')

# ========================================
# 3. INTENSYWNOŚĆ 30% - województwo pomorskie i śląskie (NAJPIERW!)
# ========================================
print('📍 Aktualizacja 30% - woj. pomorskie i śląskie:')

# Wszystkie z "pomorskie" w nazwie (w tym kujawsko- i zachodnio-, które później nadpiszemy)
count_30_pom = Gmina.objects.filter(wojewodztwo__icontains='pomorskie').update(intensywnosc_pomocy=30)

# Wszystkie ze "śląskie" (w tym dolnośląskie, które później nadpiszemy)
count_30_sla = Gmina.objects.filter(wojewodztwo__icontains='śląskie').update(intensywnosc_pomocy=30)

count_30 = count_30_pom + count_30_sla

print(f'  ✅ Wszystkie woj. z "pomorskie": {count_30_pom} gmin')
print(f'  ✅ Wszystkie woj. z "śląskie": {count_30_sla} gmin')
print(f'  📊 Razem 30%: {count_30} gmin')
print(f'  ⚠️  Uwaga: kujawsko-pomorskie i zachodniopomorskie zostaną nadpisane na 40% w następnym kroku\n')

# ========================================
# 4. INTENSYWNOŚĆ 40% - województwa centralne (NADPISUJE błędne 30%)
# ========================================
print('📍 Aktualizacja 40% - województwa centralne (nadpisuje kujawsko-pom. i zachodniopom.):')

wojewodztwa_40 = [
    'kujawsko-pomorskie',
    'lubuskie',
    'łódzkie',
    'małopolskie',
    'opolskie',
    'zachodniopomorskie',
    'mazowieckie'
]

count_40 = 0
for woj in wojewodztwa_40:
    updated = Gmina.objects.filter(wojewodztwo__icontains=woj).update(intensywnosc_pomocy=40)
    count_40 += updated
    print(f'  ✅ Woj. {woj}: {updated} gmin')

print(f'  📊 Razem 40%: {count_40} gmin\n')

# ========================================
# 5. POZOSTAŁE - wielkopolskie i dolnośląskie 25% (NADPISUJE dolnośląskie)
# ========================================
print('📍 Aktualizacja 25% - woj. wielkopolskie (poza pow. 15%) i dolnośląskie:')

# Dolnośląskie (nadpisuje błędne 30% ze śląskiego)
dolnoslaskie = Gmina.objects.filter(wojewodztwo__icontains='dolnośląsk').update(intensywnosc_pomocy=25)

# Wielkopolskie - poza powiatami z 15%
wlkp_pozostale = Gmina.objects.filter(
    wojewodztwo__icontains='wielkopolsk'
).exclude(
    powiat__icontains='obornicki'
).exclude(
    powiat__icontains='poznański'
).exclude(
    powiat__icontains='szamotulski'
).exclude(
    powiat__icontains='średzki'
).exclude(
    powiat__icontains='śremski'
).exclude(
    nazwa__icontains='Poznań', rodzaj='MNP'
).update(intensywnosc_pomocy=25)

count_25 = wlkp_pozostale + dolnoslaskie

print(f'  ✅ Woj. dolnośląskie: {dolnoslaskie} gmin')
print(f'  ✅ Woj. wielkopolskie (pozostałe): {wlkp_pozostale} gmin')
print(f'  📊 Razem 25%: {count_25} gmin\n')

# ========================================
# 6. FINALNA KOREKTA 15% - wybrane powiaty wielkopolskie + Poznań (NADPISUJE KOŃCOWO)
# ========================================
print('📍 Finalna korekta 15% - wybrane powiaty wielkopolskie + Poznań:')

# Powiaty: obornicki, poznański, szamotulski, średzki, śremski
powiaty_15_final = ['obornicki', 'poznański', 'szamotulski', 'średzki', 'śremski']
count_15_final = 0

for powiat in powiaty_15_final:
    updated = Gmina.objects.filter(powiat__icontains=powiat).update(intensywnosc_pomocy=15)
    count_15_final += updated
    print(f'  ✅ Powiat {powiat}: {updated} gmin')

# Miasto Poznań (MNP)
poznan_final = Gmina.objects.filter(nazwa__icontains='Poznań', rodzaj='MNP').update(intensywnosc_pomocy=15)
count_15_final += poznan_final
print(f'  ✅ Miasto Poznań: {poznan_final} gmin')

print(f'  📊 Razem 15% (finalna korekta): {count_15_final} gmin\n')

# ========================================
# PODSUMOWANIE KOŃCOWE
# ========================================
print('='*60)
print('✨ PODSUMOWANIE AKTUALIZACJI:')
print('='*60)
print(f'  15% (wybrane pow. wlkp. + Poznań): {count_15_powiaty} gmin')
print(f'  50% (woj. wschodnie):               {count_50} gmin')
print(f'  40% (woj. centralne):               {count_40} gmin')
print(f'  30% (woj. pomorskie i śląskie):     {count_30} gmin')
print(f'  25% (woj. wlkp. i dolnośląskie):    {count_25} gmin')
print('='*60)
print(f'  🎯 ŁĄCZNIE ZAKTUALIZOWANO: {count_15_powiaty + count_50 + count_40 + count_30 + count_25} gmin')
print('='*60)
print('\n✅ Aktualizacja zakończona pomyślnie!')
print('\n✅ Aktualizacja zakończona pomyślnie!')
