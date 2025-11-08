# PSI - Polska Strefa Inwestycji

System informacyjny dla inwestorów zawierający bazę wszystkich gmin objętych Polską Strefą Inwestycji wraz z informacjami o:
- Intensywności pomocy publicznej (0-70%)
- Minimalnych nakładach inwestycyjnych
- Różnicach dla różnych wielkości firm (Duża, Średnia, Mała, Mikro)
- Różnicach dla nowego vs istniejącego zakładu

## Technologia

- **Backend:** Django 5.2.7
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Baza danych:** SQLite
- **Python:** 3.14.0

## Struktura projektu

```
ulga/
├── psi/                    # Główna konfiguracja Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── website/                # Aplikacja Django
│   ├── models.py          # Model Gmina
│   ├── views.py           # Widoki i API endpoints
│   ├── urls.py            # Routing
│   ├── templates/         # Szablony HTML
│   └── management/        # Komendy zarządzania
├── scripts_archive/        # Archiwum skryptów jednorazowych
├── db.sqlite3             # Baza danych (2731 gmin)
├── manage.py              # Django management script
└── requirements.txt       # Zależności Python
```

## Uruchomienie

### 1. Aktywuj środowisko wirtualne:
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Uruchom serwer deweloperski:
```powershell
python manage.py runserver
```

### 3. Otwórz w przeglądarce:
```
http://127.0.0.1:8000/
```

## Funkcjonalności

### Strona główna (/)
- Landing page z informacjami o PSI

### Baza gmin (/gminy/)
- **Cascading dropdowns:** Województwo → Powiat → Gminy
- **AJAX loading:** Szybkie ładowanie danych (bez ładowania 2700+ rekordów)
- **Wyszukiwarka:** Filtrowanie po nazwie gminy
- **Rozwijane szczegóły:** Kliknij wiersz, aby zobaczyć szczegóły dla 4 typów firm

### Szczegóły dla każdej gminy:
- **Duża firma:** Podstawowa intensywność, 100% nakładów
- **Średnia firma:** +10pp intensywności, 10% nakładów (90% zniżka)
- **Mała firma:** +20pp intensywności, 5% nakładów (95% zniżka)
- **Mikro firma:** +20pp intensywności, 2% nakładów (98% zniżka)

Każdy typ pokazuje różnicę między **nowym zakładem** (100%) a **istniejącym zakładem** (50% nakładów).

### API Endpoints

- `GET /api/powiaty/?wojewodztwo={name}` - Lista powiatów dla województwa
- `GET /api/gminy/?wojewodztwo={name}&powiat={name}&search={query}` - Lista gmin z filtrowaniem

## Dane

### Baza danych zawiera:
- **2731 gmin** z całej Polski
- **16 województw**
- **~380 powiatów**

### Źródła danych:
- `baza.xlsx` - Główne dane gmin (kod TERYT, nazwy, rodzaje)
- `bezrobocie.xlsx` - Minimalne nakłady inwestycyjne według województw i powiatów

### Specjalne przypadki:
- **Warszawa:** 0% intensywności (brak wsparcia PSI)
- **Gminy tracące funkcje:** 10 mln PLN minimalnych nakładów (581 gmin)
- **Granica wschodnia:** 10 mln PLN minimalnych nakładów (197 gmin w 12 powiatach)

## Maintenance

### Aktualizacja danych
Jeśli potrzebujesz zaktualizować dane, edytuj bazę przez Django admin:

```powershell
python manage.py createsuperuser
python manage.py runserver
```

Następnie wejdź na: `http://127.0.0.1:8000/admin/`

### Migracje bazy danych
```powershell
python manage.py makemigrations
python manage.py migrate
```

## Deployment

Pliki konfiguracyjne deployment znajdują się w katalogu `deploy/`

## Historia zmian

- **v1.0** - Podstawowa lista gmin z Django templates
- **v2.0** - Import danych z Excel, wsparcie dla polskich znaków
- **v3.0** - Rozwijane wiersze z szczegółami dla typów firm
- **v4.0** - AJAX z cascading dropdowns (optymalizacja wydajności)

## Autor

Projekt PSI - System informacji o Polskiej Strefie Inwestycji
