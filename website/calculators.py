"""
Moduł z logiką obliczeniową dla kalkulatora PSI (Polska Strefa Inwestycji).
"""
from decimal import Decimal
from typing import Dict, Any


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

    def oblicz_maksymalna_pomoc(self) -> Decimal:
        """
        Oblicza maksymalną kwotę pomocy publicznej.

        Returns:
            Maksymalna kwota pomocy w PLN
        """
        intensywnosc = self.oblicz_intensywnosc_pomocy()

        # Maksymalna pomoc = wartość inwestycji × intensywność pomocy
        maksymalna_pomoc = self.wartosc_inwestycji * (intensywnosc / Decimal('100'))

        return maksymalna_pomoc.quantize(Decimal('0.01'))

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

    def oblicz_wyniki(self) -> Dict[str, Any]:
        """
        Przeprowadza wszystkie obliczenia i zwraca kompleksowy wynik.

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
                'maksymalna_pomoc': self.oblicz_maksymalna_pomoc() if kwalifikuje_sie else Decimal('0'),
                'okres_waznosci': self.oblicz_okres_waznosci() if kwalifikuje_sie else 0,
                'liczba_kryteriow': self.pobierz_liczbe_kryteriow(),
            }
        }

        # Dodaj komunikat o przyczynie braku kwalifikacji
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
