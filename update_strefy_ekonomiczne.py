"""
Skrypt do aktualizacji pola strefa_ekonomiczna w bazie danych
na podstawie przypisania powiatów do Specjalnych Stref Ekonomicznych
"""

import os
import sys

import django

# Konfiguracja Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "psi.settings")
django.setup()

from website.models import Gmina

# Mapowanie powiatów do SSE
STREFY_EKONOMICZNE = {
    "Kamiennogórska Specjalna Strefa Ekonomiczna Małej Przedsiębiorczości": [
        "bolesławiecki",
        "jeleniogórski",
        "kamiennogórski",
        "karkonoski",
        "kępiński",
        "lubański",
        "lwówecki",
        "milicki",
        "ostrowski",
        "trzebnicki",
        "zgorzelecki",
        "Jelenia Góra",
    ],
    "Katowicka Specjalna Strefa Ekonomiczna": [
        "będziński",
        "bielski",
        "bieruńsko-lędziński",
        "cieszyński",
        "częstochowski",
        "gliwicki",
        "głubczycki",
        "kędzierzyńsko-kozielski",
        "kłobucki",
        "krapkowicki",
        "lubliniecki",
        "mikołowski",
        "myszkowski",
        "oleski",
        "prudnicki",
        "pszczyński",
        "raciborski",
        "rybnicki",
        "strzelecki",
        "tarnogórski",
        "wodzisławski",
        "zawierciański",
        "żywiecki",
        "Bielsko-Biała",
        "Bytom",
        "Chorzów",
        "Częstochowa",
        "Dąbrowa Górnicza",
        "Gliwice",
        "Jastrzębie-Zdrój",
        "Jaworzno",
        "Katowice",
        "Mysłowice",
        "Piekary Śląskie",
        "Ruda Śląska",
        "Rybnik",
        "Siemianowice Śląskie",
        "Sosnowiec",
        "Świętochłowice",
        "Tychy",
        "Zabrze",
        "Żory",
    ],
    "Kostrzyńsko-Słubicka Specjalna Strefa Ekonomiczna": [
        "czarnkowsko-trzcianecki",
        "chodzieski",
        "choszczeński",
        "goleniowski",
        "gorzowski",
        "grodziski",
        "gryficki",
        "gryfiński",
        "gnieźnieński",
        "kamieński",
        "kościański",
        "krośnieński",
        "łobeski",
        "międzychodzki",
        "międzyrzecki",
        "myśliborski",
        "nowosolski",
        "nowotomyski",
        "obornicki",
        "pilski",
        "policki",
        "poznański",
        "pyrzycki",
        "słubicki",
        "stargardzki",
        "strzelecko-drezdenecki",
        "sulęciński",
        "szamotulski",
        "świebodziński",
        "wągrowiecki",
        "wolsztyński",
        "wschowski",
        "zielonogórski",
        "żagański",
        "żarski",
        "Gorzów Wielkopolski",
        "Poznań",
        "Szczecin",
        "Świnoujście",
        "Zielona Góra",
    ],
    "Krakowski Park Technologiczny": [
        "bocheński",
        "brzeski",
        "chrzanowski",
        "dąbrowski",
        "gorlicki",
        "jędrzejowski",
        "krakowski",
        "limanowski",
        "miechowski",
        "myślenicki",
        "nowosądecki",
        "nowotarski",
        "olkuski",
        "oświęcimski",
        "proszowicki",
        "suski",
        "tarnowski",
        "tatrzański",
        "wadowicki",
        "wielicki",
        "Kraków",
        "Nowy Sącz",
        "Tarnów",
    ],
    "Legnicka Specjalna Strefa Ekonomiczna": [
        "głogowski",
        "górowski",
        "legnicki",
        "lubiński",
        "polkowicki",
        "średzki",
        "wołowski",
        "złotoryjski",
        "Legnica",
    ],
    "Łódzka Specjalna Strefa Ekonomiczna": [
        "bełchatowski",
        "brzeziński",
        "gostyniński",
        "grodziski",
        "kaliski",
        "kolski",
        "koniński",
        "kutnowski",
        "legionowski",
        "łaski",
        "łęczycki",
        "łowicki",
        "łódzki wschodni",
        "opoczyński",
        "ostrzeszowski",
        "otwocki",
        "pabianicki",
        "pajęczański",
        "piaseczyński",
        "piotrkowski",
        "płocki",
        "poddębicki",
        "pruszkowski",
        "radomszczański",
        "rawski",
        "sieradzki",
        "sierpecki",
        "skierniewicki",
        "sochaczewski",
        "tomaszowski",
        "turecki",
        "warszawski zachodni",
        "wieluński",
        "wieruszowski",
        "wołomiński",
        "zduńskowolski",
        "zgierski",
        "żyrardowski",
        "Kalisz",
        "Konin",
        "Łódź",
        "Piotrków Trybunalski",
        "Płock",
        "Skierniewice",
        "Warszawa",
    ],
    "Specjalna Strefa Ekonomiczna Euro-Park Mielec": [
        "bieszczadzki",
        "brzozowski",
        "dębicki",
        "jarosławski",
        "jasielski",
        "kolbuszowski",
        "krośnieński",
        "leski",
        "leżajski",
        "lubaczowski",
        "lubartowski",
        "lubelski",
        "łańcucki",
        "mielecki",
        "przeworski",
        "ropczycko-sędziszowski",
        "rzeszowski",
        "sanocki",
        "strzyżowski",
        "świdnicki",
        "Lublin",
        "Krosno",
        "Rzeszów",
    ],
    "Pomorska Specjalna Strefa Ekonomiczna": [
        "aleksandrowski",
        "brodnicki",
        "bydgoski",
        "chełmiński",
        "chojnicki",
        "gdański",
        "golubsko-dobrzyński",
        "grudziądzki",
        "inowrocławski",
        "kartuski",
        "kwidzyński",
        "lipnowski",
        "malborski",
        "mogileński",
        "nakielski",
        "nowodworski",
        "pucki",
        "radziejowski",
        "rypiński",
        "sępoleński",
        "starogardzki",
        "sztumski",
        "świecki",
        "tczewski",
        "toruński",
        "tucholski",
        "wąbrzeski",
        "wejherowski",
        "włocławski",
        "żniński",
        "Bydgoszcz",
        "Gdańsk",
        "Gdynia",
        "Grudziądz",
        "Sopot",
        "Toruń",
        "Włocławek",
    ],
    "Słupska Specjalna Strefa Ekonomiczna": [
        "białogardzki",
        "bytowski",
        "człuchowski",
        "drawski",
        "kołobrzeski",
        "koszaliński",
        "kościerski",
        "lęborski",
        "sławieński",
        "słupski",
        "szczecinecki",
        "świdwiński",
        "wałecki",
        "złotowski",
        "Koszalin",
        "Słupsk",
    ],
    "Specjalna Strefa Ekonomiczna Starachowice": [
        "buski",
        "kazimierski",
        "kielecki",
        "konecki",
        "opatowski",
        "ostrowiecki",
        "pińczowski",
        "przysuski",
        "puławski",
        "radomski",
        "sandomierski",
        "skarżyski",
        "starachowicki",
        "staszowski",
        "szydłowiecki",
        "włoszczowski",
        "Kielce",
    ],
    "Suwalska Specjalna Strefa Ekonomiczna": [
        "augustowski",
        "białostocki",
        "bielski",
        "ełcki",
        "gołdapski",
        "grajewski",
        "hajnowski",
        "kolneński",
        "łomżyński",
        "łosicki",
        "moniecki",
        "ostrowski",
        "sejneński",
        "siemiatycki",
        "sokołowski",
        "sokólski",
        "suwalski",
        "węgrowski",
        "wysokomazowiecki",
        "zambrowski",
        "Białystok",
        "Łomża",
        "Suwałki",
    ],
    "Tarnobrzeska Specjalna Strefa Ekonomiczna EURO-PARK WISŁOSAN": [
        "bialski",
        "białobrzeski",
        "biłgorajski",
        "chełmski",
        "garwoliński",
        "grójecki",
        "hrubieszowski",
        "janowski",
        "kozienicki",
        "krasnostawski",
        "kraśnicki",
        "lipski",
        "łęczyński",
        "łukowski",
        "miński",
        "niżański",
        "opolski",
        "parczewski",
        "przemyski",
        "radzyński",
        "rycki",
        "siedlecki",
        "stalowowolski",
        "tarnobrzeski",
        "tomaszowski",
        "włodawski",
        "zamojski",
        "zwoleński",
        "Biała Podlaska",
        "Chełm",
        "Przemyśl",
        "Radom",
        "Siedlce",
        "Tarnobrzeg",
        "Zamość",
    ],
    "Wałbrzyska Specjalna Strefa Ekonomiczna INVEST-PARK": [
        "brzeski",
        "dzierżoniowski",
        "gostyński",
        "jarociński",
        "jaworski",
        "kluczborski",
        "kłodzki",
        "krotoszyński",
        "leszczyński",
        "namysłowski",
        "nyski",
        "oleśnicki",
        "oławski",
        "opolski",
        "pleszewski",
        "rawicki",
        "słupecki",
        "strzeliński",
        "średzki",
        "śremski",
        "świdnicki",
        "wałbrzyski",
        "wrocławski",
        "wrzesiński",
        "ząbkowicki",
        "Leszno",
        "Opole",
        "Wałbrzych",
        "Wrocław",
    ],
    "Warmińsko-Mazurska Specjalna Strefa Ekonomiczna": [
        "bartoszycki",
        "braniewski",
        "ciechanowski",
        "działdowski",
        "elbląski",
        "giżycki",
        "iławski",
        "kętrzyński",
        "lidzbarski",
        "makowski",
        "mławski",
        "mrągowski",
        "nidzicki",
        "nowodworski",
        "nowomiejski",
        "olecki",
        "olsztyński",
        "ostrołęcki",
        "ostródzki",
        "piski",
        "płoński",
        "przasnyski",
        "pułtuski",
        "szczycieński",
        "węgorzewski",
        "wyszkowski",
        "żuromiński",
        "Elbląg",
        "Olsztyn",
        "Ostrołęka",
    ],
}


def normalizuj_nazwe(nazwa):
    """
    Normalizuje nazwę powiatu, usuwając zbędne sufiksy i województwa w nawiasach
    """
    nazwa = nazwa.lower().strip()

    # Usuń informacje o województwie w nawiasach
    if "(woj." in nazwa:
        nazwa = nazwa.split("(woj.")[0].strip()

    # Usuń typ powiatu jeśli istnieje na końcu
    suffiksy = [" powiat", " m.", " miasto"]
    for suffiks in suffiksy:
        if nazwa.endswith(suffiks):
            nazwa = nazwa[: -len(suffiks)].strip()

    return nazwa


def main():
    print("=" * 80)
    print("AKTUALIZACJA STREF EKONOMICZNYCH")
    print("=" * 80)

    # Stwórz odwrotne mapowanie: powiat -> strefa
    powiat_do_strefy = {}
    for strefa, powiaty in STREFY_EKONOMICZNE.items():
        for powiat in powiaty:
            powiat_norm = normalizuj_nazwe(powiat)
            if powiat_norm in powiat_do_strefy:
                print(
                    f"UWAGA: Powiat '{powiat}' pojawia się w więcej niż jednej strefie!"
                )
            powiat_do_strefy[powiat_norm] = strefa

    print(
        f"\nZaładowano {len(powiat_do_strefy)} powiatów w {len(STREFY_EKONOMICZNE)} strefach"
    )
    print(f"Liczba gmin w bazie: {Gmina.objects.count()}")

    # Statystyki
    zaktualizowane = 0
    nie_znaleziono = []

    # Pobierz wszystkie gminy
    gminy = Gmina.objects.all()

    for gmina in gminy:
        powiat_norm = normalizuj_nazwe(gmina.powiat)

        if powiat_norm in powiat_do_strefy:
            strefa = powiat_do_strefy[powiat_norm]
            gmina.strefa_ekonomiczna = strefa
            gmina.save(update_fields=["strefa_ekonomiczna"])
            zaktualizowane += 1
        else:
            nie_znaleziono.append((gmina.powiat, gmina.wojewodztwo))

    print(f"\n✓ Zaktualizowano: {zaktualizowane} gmin")

    if nie_znaleziono:
        print(f"\n⚠ Nie znaleziono strefy dla {len(nie_znaleziono)} gmin:")
        # Wyświetl tylko unikalne powiaty
        unikalne = list(set(nie_znaleziono))
        unikalne.sort()
        for powiat, woj in unikalne[:20]:  # Pokaż pierwsze 20
            print(f"  - {powiat} (woj. {woj})")
        if len(unikalne) > 20:
            print(f"  ... i {len(unikalne) - 20} więcej")

    # Weryfikacja
    print("\n" + "=" * 80)
    print("WERYFIKACJA")
    print("=" * 80)

    gminy_ze_strefa = Gmina.objects.filter(strefa_ekonomiczna__isnull=False).count()
    gminy_bez_strefy = Gmina.objects.filter(strefa_ekonomiczna__isnull=True).count()

    print(f"Gminy ze strefą: {gminy_ze_strefa}")
    print(f"Gminy bez strefy: {gminy_bez_strefy}")

    if gminy_bez_strefy == 0:
        print("\n✓ Wszystkie gminy mają przypisaną strefę ekonomiczną!")
    else:
        print(f"\n⚠ {gminy_bez_strefy} gmin nie ma przypisanej strefy")

    # Pokaż podział na strefy
    print("\n" + "=" * 80)
    print("STATYSTYKI WEDŁUG STREF")
    print("=" * 80)

    from django.db.models import Count

    strefy_stats = (
        Gmina.objects.values("strefa_ekonomiczna")
        .annotate(liczba=Count("id"))
        .order_by("-liczba")
    )

    for stat in strefy_stats:
        if stat["strefa_ekonomiczna"]:
            print(f"{stat['liczba']:4d} - {stat['strefa_ekonomiczna']}")
        else:
            print(f"{stat['liczba']:4d} - (brak strefy)")

    print("\n" + "=" * 80)
    print("ZAKOŃCZONO")
    print("=" * 80)


if __name__ == "__main__":
    main()
