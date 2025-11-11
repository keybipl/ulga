# Instrukcja: Pliki graficzne dla strony

## 1. Logo główne strony (ulga2.png)

### Wymagania:
- **Nazwa pliku**: `ulga2.png`
- **Format**: PNG z przezroczystym tłem
- **Wymiary**: Zalecane 200px × 60px (proporcje 10:3)
- **Rozdzielczość**: Min. 200x60px, idealnie 400x120px (2x dla Retina)
- **Kolor tła**: Przezroczysty
- **Optymalizacja**: Skompresowany PNG

### Responsive:
- Desktop: 60px wysokości
- Tablet: 55px wysokości  
- Mobile: 45px wysokości
- Fallback: https://kssse.pl/psi.png

---

## 2. Logo PSI (psi-logo.png)

### Wymagania:
- **Nazwa pliku**: `psi-logo.png`
- **Format**: PNG z przezroczystym tłem lub białym tłem
- **Wymiary**: Zalecane szerokość 400-600px
- **Maksymalna wysokość**: 200px (desktop), 150px (mobile)
- **Kolor tła**: Preferowane przezroczyste lub białe
- **Optymalizacja**: Skompresowany PNG

### Gdzie używane:
- Strona "O Programie" - sekcja pod nagłówkiem
- Pokazuje oficjalne logo programu rządowego PSI

### Fallback:
- https://kssse.pl/psi.png

---

## Struktura katalogów:

```
website/static/images/
├── ulga2.png          ← Logo główne strony (header)
├── psi-logo.png       ← Logo programu PSI (strona O Programie)
├── README.md          ← Instrukcje (stary plik)
└── LOGO-INFO.md       ← Ten plik (nowy)
```

## Jak dodać logo PSI:

1. Pobierz oficjalne logo PSI z:
   - https://www.gov.pl/web/rozwoj-technologia
   - Lub ze strony lokalnej strefy ekonomicznej
   
2. Zapisz jako: `psi-logo.png`

3. Umieść w: `c:\Users\Ania\Documents\ulga\website\static\images\`

4. Odśwież stronę "O Programie" (Ctrl+F5)

## Alternatywnie (tymczasowo):

Jeśli nie masz jeszcze logo, strona użyje automatycznie fallback z:
`https://kssse.pl/psi.png`

## Uwagi:

- Zachowaj oryginalne proporcje logo
- Nie nadpisuj pliku `ulga2.png` (to logo główne strony)
- Po dodaniu nowych plików na produkcji uruchom: `python manage.py collectstatic --settings=psi.settings_prod`
