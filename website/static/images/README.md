# Instrukcja: Logo dla strony

## Wymagania logo:

1. **Nazwa pliku**: `logo.png`
2. **Format**: PNG z przezroczystym tłem
3. **Wymiary**: Zalecane 200px szerokości × 60px wysokości (proporcje 10:3)
4. **Rozdzielczość**: Min. 200x60px, idealnie 400x120px (2x dla Retina)
5. **Kolor tła**: Przezroczysty (transparent)
6. **Optymalizacja**: Skompresowany PNG (TinyPNG lub podobne)

## Gdzie umieścić logo:

Umieść plik `logo.png` w tym katalogu:
```
website/static/images/logo.png
```

## Uwagi techniczne:

- Logo będzie skalowane automatycznie do 60px wysokości na desktop
- Na mobile: 45px wysokości
- Na tablet: 55px wysokości
- Zachowana proporcja szerokość/wysokość (aspect ratio)
- Fallback: jeśli plik nie istnieje, zostanie użyte logo z https://kssse.pl/psi.png

## Jak dodać logo:

1. Przygotuj logo w formacie PNG z przezroczystym tłem
2. Nazwij plik: `logo.png`
3. Skopiuj do katalogu: `c:\Users\Ania\Documents\ulga\website\static\images\`
4. Logo będzie automatycznie załadowane po odświeżeniu strony
