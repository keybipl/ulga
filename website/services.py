"""
Serwisy zewnętrzne dla aplikacji website.
"""
import requests
from decimal import Decimal
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class NBPService:
    """
    Serwis do komunikacji z API Narodowego Banku Polskiego.
    """

    BASE_URL = 'https://api.nbp.pl/api/exchangerates/rates/a/eur'
    TIMEOUT = 10  # sekundy

    @classmethod
    def get_euro_exchange_rate(cls) -> Dict[str, Any]:
        """
        Pobiera aktualny kurs EUR z API NBP.

        Returns:
            Dict zawierający:
                - 'rate': Decimal - kurs EUR/PLN
                - 'date': str - data kursu (YYYY-MM-DD)
                - 'table': str - typ tabeli ('A')

        Raises:
            Exception: gdy nie udało się pobrać kursu
        """
        # Próbuj dzisiejszy kurs, potem ostatni dostępny
        urls = [
            f"{cls.BASE_URL}/today/",
            f"{cls.BASE_URL}/last/1/"
        ]

        for url in urls:
            try:
                response = requests.get(url, timeout=cls.TIMEOUT)
                response.raise_for_status()
                data = response.json()

                # Struktura: {'rates': [{'no': '...', 'effectiveDate': '...', 'mid': 4.25}]}
                rate_data = data['rates'][0]

                return {
                    'rate': Decimal(str(rate_data['mid'])),
                    'date': rate_data['effectiveDate'],
                    'table': data['table']
                }
            except (requests.RequestException, KeyError, ValueError, IndexError) as e:
                logger.warning(f"Nie udało się pobrać kursu z {url}: {e}")
                continue

        # Jeśli wszystkie próby zawiodły
        logger.error("Nie udało się pobrać kursu EUR z API NBP")
        raise Exception("Nie można pobrać aktualnego kursu EUR z NBP")
