"""
Moduł z logiką obliczeniową dla kalkulatora PSI (Polska Strefa Inwestycji).
"""
from decimal import Decimal
from typing import Dict, Any, Optional


class PSICalculator:
    """
    Kalkulator pomocy publicznej w ramach Polskiej Strefy Inwestycji.
    """

    # Mnożniki minimalnych nakładów dla różnych wielkości firm
    NAKLADY_MULTIPLIERS = {
        'duza': Decimal('1.0'),      # 100% bazowej wartości
        'srednia': Decimal('0.1'),   # 10% bazowej wartości
        'mala': Decimal('0.05'),     # 5% bazowej wartości
        'mikro': Decimal('0.02'),    # 2% bazowej wartości
    }

    # Bonusy do intensywności pomocy dla różnych wielkości firm (w punktach procentowych)
    INTENSYWNOSC_BONUSES = {
        'duza': Decimal('0'),    # +0pp
        'srednia': Decimal('10'), # +10pp
        'mala': Decimal('20'),   # +20pp
        'mikro': Decimal('20'),  # +20pp
    }

    # Mnożnik dla istniejącego zakładu (50% progu)
    ISTNIEJACY_ZAKLAD_MULTIPLIER = Decimal('0.5')

    # Progi dla segmentacji projektów (w EUR)
    PROG_MALY_PROJEKT_EUR = Decimal('55000000')      # 55 mln EUR
    PROG_BARDZO_DUZY_PROJEKT_EUR = Decimal('110000000')  # 110 mln EUR

    def __init__(self, gmina, wielkosc_firmy: str, nowy_zaklad: bool,
                 wartosc_inwestycji: Decimal, tylko_bpo: bool = False):
        """
        Inicjalizacja kalkulatora.

        Args:
            gmina: Obiekt modelu Gmina
            wielkosc_firmy: 'mikro', 'mala', 'srednia', 'duza'
            nowy_zaklad: True dla nowego zakładu, False dla istniejącego
            wartosc_inwestycji: Wartość inwestycji w PLN
            tylko_bpo: True jeśli działalność TYLKO w sektorze BPO/SSSE
        """
        self.gmina = gmina
        self.wielkosc_firmy = wielkosc_firmy.lower()
        self.nowy_zaklad = nowy_zaklad
        self.wartosc_inwestycji = Decimal(str(wartosc_inwestycji))
        self.tylko_bpo = tylko_bpo

    def oblicz_intensywnosc_pomocy(self) -> Decimal:
        """
        Oblicza intensywność pomocy (%) dla danej firmy.

        Returns:
            Intensywność pomocy w procentach (np. Decimal('50.00'))
        """
        bazowa_intensywnosc = self.gmina.intensywnosc_pomocy
        bonus = self.INTENSYWNOSC_BONUSES.get(self.wielkosc_firmy, Decimal('0'))

        intensywnosc = bazowa_intensywnosc + bonus

        # Maksymalna intensywność to 70%
        return min(intensywnosc, Decimal('70'))

    def _przelicz_na_eur(self, kwota_pln: Decimal, kurs_euro: Decimal) -> Decimal:
        """
        Przelicza kwotę z PLN na EUR.

        Args:
            kwota_pln: Kwota w PLN
            kurs_euro: Kurs EUR/PLN

        Returns:
            Kwota w EUR
        """
        if kurs_euro == 0:
            raise ValueError("Kurs EUR nie może być równy 0")

        return (kwota_pln / kurs_euro).quantize(Decimal('0.01'))

    def oblicz_minimalne_naklady(self) -> Decimal:
        """
        Oblicza minimalne nakłady inwestycyjne wymagane dla kwalifikacji.

        Returns:
            Minimalne nakłady w PLN
        """
        # Dla BPO stosujemy progi jak dla małej firmy (-95%)
        if self.tylko_bpo:
            mnoznik = self.NAKLADY_MULTIPLIERS['mala']
        else:
            mnoznik = self.NAKLADY_MULTIPLIERS.get(self.wielkosc_firmy, Decimal('1.0'))

        minimalne_naklady = self.gmina.minimalne_naklady * mnoznik

        # Dla istniejącego zakładu próg jest o 50% niższy
        if not self.nowy_zaklad:
            minimalne_naklady *= self.ISTNIEJACY_ZAKLAD_MULTIPLIER

        return minimalne_naklady

    def oblicz_maksymalna_pomoc(self, kurs_euro: Optional[Decimal] = None) -> Decimal:
        """
        Oblicza maksymalną kwotę pomocy publicznej.
        Dla projektów 55-110 mln EUR stosuje wzór progresywny.

        Args:
            kurs_euro: Opcjonalny kurs EUR/PLN dla projektów wymagających segmentacji

        Returns:
            Maksymalna kwota pomocy w PLN
        """
        # Jeśli kurs nie podany → stara logika (backward compatibility)
        if kurs_euro is None:
            intensywnosc = self.oblicz_intensywnosc_pomocy()
            maksymalna_pomoc = self.wartosc_inwestycji * (intensywnosc / Decimal('100'))
            return maksymalna_pomoc.quantize(Decimal('0.01'))

        # Przelicz wartość na EUR
        wartosc_eur = self._przelicz_na_eur(self.wartosc_inwestycji, kurs_euro)

        # Segment A: ≤55 mln EUR (mały projekt)
        if wartosc_eur <= self.PROG_MALY_PROJEKT_EUR:
            intensywnosc = self.oblicz_intensywnosc_pomocy()
            maksymalna_pomoc = self.wartosc_inwestycji * (intensywnosc / Decimal('100'))
            return maksymalna_pomoc.quantize(Decimal('0.01'))

        # Segment B: 55-110 mln EUR (PROGRESYWNY)
        elif wartosc_eur <= self.PROG_BARDZO_DUZY_PROJEKT_EUR:
            # KRYTYCZNE: Zawsze intensywność bazowa (bez bonusów MŚP)
            R = self.gmina.intensywnosc_pomocy / Decimal('100')

            # A = koszty do 55 mln EUR (w PLN)
            A_pln = self.PROG_MALY_PROJEKT_EUR * kurs_euro

            # B = koszty powyżej 55 mln EUR (w PLN)
            B_pln = self.wartosc_inwestycji - A_pln

            # Wzór: I = R × (A + 0,5 × B)
            maksymalna_pomoc = R * (A_pln + Decimal('0.5') * B_pln)
            return maksymalna_pomoc.quantize(Decimal('0.01'))

        # Segment C: >110 mln EUR (bardzo duży projekt)
        else:
            intensywnosc = self.oblicz_intensywnosc_pomocy()
            maksymalna_pomoc = self.wartosc_inwestycji * (intensywnosc / Decimal('100'))
            return maksymalna_pomoc.quantize(Decimal('0.01'))

    def _okresl_segment_projektu(self, kurs_euro: Decimal) -> str:
        """
        Określa segment projektu na podstawie wartości w EUR.

        Args:
            kurs_euro: Kurs EUR/PLN

        Returns:
            'maly' | 'progresywny' | 'bardzo_duzy'
        """
        wartosc_eur = self._przelicz_na_eur(self.wartosc_inwestycji, kurs_euro)

        if wartosc_eur <= self.PROG_MALY_PROJEKT_EUR:
            return 'maly'
        elif wartosc_eur <= self.PROG_BARDZO_DUZY_PROJEKT_EUR:
            return 'progresywny'
        else:
            return 'bardzo_duzy'

    def czy_kwalifikuje_sie(self) -> bool:
        """
        Sprawdza czy projekt spełnia minimalne wymagania.

        Returns:
            True jeśli projekt się kwalifikuje, False w przeciwnym razie
        """
        # Gminy z intensywnością 0% (np. Warszawa) nie kwalifikują się
        if self.gmina.intensywnosc_pomocy == 0:
            return False

        # Duże przedsiębiorstwa w istniejących zakładach w województwie wielkopolskim i dolnośląskim
        # nie mogą otrzymać wsparcia
        if (self.wielkosc_firmy == 'duza' and
            not self.nowy_zaklad and
            self.gmina.wojewodztwo.lower() in ['wielkopolskie', 'dolnośląskie']):
            return False

        minimalne_naklady = self.oblicz_minimalne_naklady()

        return self.wartosc_inwestycji >= minimalne_naklady

    def oblicz_okres_waznosci(self) -> int:
        """
        Oblicza okres ważności decyzji o wsparciu (w latach).

        Returns:
            Liczba lat (15, 14 lub 12)
        """
        intensywnosc = self.gmina.intensywnosc_pomocy

        if intensywnosc >= 50:
            return 15
        elif intensywnosc >= 30:
            return 14
        else:
            return 12

    def pobierz_liczbe_kryteriow(self) -> int:
        """
        Pobiera wymaganą liczbę kryteriów jakościowych.

        Returns:
            Liczba wymaganych kryteriów (4, 5 lub 6)
        """
        return self.gmina.get_liczba_kryteriow_jakosciowych()

    def oblicz_wyniki(self, kurs_euro: Optional[Decimal] = None,
                      data_kursu: Optional[str] = None) -> Dict[str, Any]:
        """
        Przeprowadza wszystkie obliczenia i zwraca kompleksowy wynik.

        Args:
            kurs_euro: Kurs EUR/PLN (opcjonalny dla małych projektów)
            data_kursu: Data kursu w formacie YYYY-MM-DD

        Returns:
            Słownik z wynikami obliczeń
        """
        kwalifikuje_sie = self.czy_kwalifikuje_sie()
        intensywnosc = self.oblicz_intensywnosc_pomocy()
        minimalne_naklady = self.oblicz_minimalne_naklady()

        wyniki = {
            'kwalifikuje_sie': kwalifikuje_sie,
            'gmina': {
                'nazwa': self.gmina.nazwa,
                'powiat': self.gmina.powiat,
                'wojewodztwo': self.gmina.wojewodztwo,
                'intensywnosc_bazowa': self.gmina.intensywnosc_pomocy,
            },
            'parametry': {
                'wielkosc_firmy': self.wielkosc_firmy,
                'nowy_zaklad': self.nowy_zaklad,
                'wartosc_inwestycji': self.wartosc_inwestycji,
                'tylko_bpo': self.tylko_bpo,
            },
            'wyniki_obliczen': {
                'intensywnosc_pomocy': intensywnosc,
                'minimalne_naklady': minimalne_naklady,
                'maksymalna_pomoc': Decimal('0'),  # Będzie uzupełnione poniżej
                'okres_waznosci': self.oblicz_okres_waznosci() if kwalifikuje_sie else 0,
                'liczba_kryteriow': self.pobierz_liczbe_kryteriow(),
            }
        }

        # Jeśli projekt się nie kwalifikuje, zwróć podstawowe wyniki
        if not kwalifikuje_sie:
            if self.gmina.intensywnosc_pomocy == 0:
                wyniki['komunikat'] = 'Wybrana gmina nie kwalifikuje się do wsparcia w ramach PSI (intensywność pomocy 0%).'
            elif (self.wielkosc_firmy == 'duza' and
                  not self.nowy_zaklad and
                  self.gmina.wojewodztwo.lower() in ['wielkopolskie', 'dolnośląskie']):
                wyniki['komunikat'] = f'Wsparcie nie jest możliwe dla dużych przedsiębiorstw w istniejących zakładach w tym województwie. Duże przedsiębiorstwa mogą otrzymać wsparcie tylko dla nowych zakładów w tej lokalizacji.'
            else:
                wyniki['komunikat'] = f'Wartość inwestycji ({self.wartosc_inwestycji:,.2f} PLN) jest niższa niż wymagane minimalne nakłady ({minimalne_naklady:,.2f} PLN).'
            return wyniki

        # Projekt się kwalifikuje - oblicz maksymalną pomoc
        # Jeśli brak kursu → stara logika (bez segmentacji)
        if kurs_euro is None:
            wyniki['wyniki_obliczen']['maksymalna_pomoc'] = self.oblicz_maksymalna_pomoc()
            return wyniki

        # Nowa logika z segmentacją projektów
        segment = self._okresl_segment_projektu(kurs_euro)
        wartosc_eur = self._przelicz_na_eur(self.wartosc_inwestycji, kurs_euro)

        # Dodaj informacje o kursie NBP
        wyniki['kurs_nbp'] = {
            'kurs': kurs_euro,
            'data': data_kursu,
            'wartosc_inwestycji_eur': wartosc_eur,
        }
        wyniki['segment_projektu'] = segment

        # Oblicz pomoc z uwzględnieniem segmentu
        wyniki['wyniki_obliczen']['maksymalna_pomoc'] = self.oblicz_maksymalna_pomoc(kurs_euro)

        # Dodatkowe dane dla segmentu progresywnego (55-110 mln EUR)
        if segment == 'progresywny':
            A_eur = self.PROG_MALY_PROJEKT_EUR
            B_eur = wartosc_eur - A_eur
            A_pln = A_eur * kurs_euro
            B_pln = B_eur * kurs_euro

            wyniki['dane_progresywne'] = {
                'intensywnosc_dla_duzego': self.gmina.intensywnosc_pomocy,
                'A_eur': A_eur,
                'B_eur': B_eur,
                'A_pln': A_pln,
                'B_pln': B_pln,
            }

        # Komunikat dla bardzo dużych projektów (>110 mln EUR)
        if segment == 'bardzo_duzy':
            wyniki['wymaga_notyfikacji_ke'] = True
            wyniki['komunikat_ke'] = (
                'Projekty inwestycyjne o wartości przekraczającej 110 mln EUR '
                'podlegają obowiązkowi notyfikacji Komisji Europejskiej zgodnie '
                'z przepisami o pomocy regionalnej.'
            )
            # Nie wyświetlamy maksymalnej pomocy dla projektów wymagających notyfikacji
            wyniki['wyniki_obliczen']['maksymalna_pomoc'] = None

        return wyniki
