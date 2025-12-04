/**
 * Kalkulator PSI - Kaskadowe dropdowny i walidacja formularza
 */

document.addEventListener('DOMContentLoaded', function() {
    // Pobierz elementy formularza
    const wojewodztwoSelect = document.getElementById('id_wojewodztwo');
    const powiatSelect = document.getElementById('id_powiat');
    const gminaSelect = document.getElementById('id_gmina');
    const form = document.getElementById('kalkulatorForm');
    const wynikiContainer = document.getElementById('wynikiContainer');

    // Przewiń do wyników po załadowaniu strony (jeśli są)
    if (wynikiContainer) {
        setTimeout(() => {
            wynikiContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
    }

    // Obsługa zmiany województwa
    if (wojewodztwoSelect) {
        wojewodztwoSelect.addEventListener('change', function() {
            const wojewodztwo = this.value;

            // Resetuj powiat i gminę
            powiatSelect.innerHTML = '<option value="">-- Ładowanie... --</option>';
            powiatSelect.disabled = true;
            gminaSelect.innerHTML = '<option value="">-- Najpierw wybierz powiat --</option>';
            gminaSelect.disabled = true;

            if (!wojewodztwo) {
                powiatSelect.innerHTML = '<option value="">-- Najpierw wybierz województwo --</option>';
                return;
            }

            // Pobierz powiaty dla wybranego województwa
            fetch(`/api/powiaty/?wojewodztwo=${encodeURIComponent(wojewodztwo)}`)
                .then(response => response.json())
                .then(data => {
                    powiatSelect.innerHTML = '<option value="">-- Wybierz powiat --</option>';
                    data.powiaty.forEach(powiat => {
                        const option = document.createElement('option');
                        option.value = powiat;
                        option.textContent = powiat;
                        powiatSelect.appendChild(option);
                    });
                    powiatSelect.disabled = false;
                })
                .catch(error => {
                    console.error('Błąd pobierania powiatów:', error);
                    powiatSelect.innerHTML = '<option value="">-- Błąd ładowania --</option>';
                });
        });
    }

    // Obsługa zmiany powiatu
    if (powiatSelect) {
        powiatSelect.addEventListener('change', function() {
            const wojewodztwo = wojewodztwoSelect.value;
            const powiat = this.value;

            // Resetuj gminę
            gminaSelect.innerHTML = '<option value="">-- Ładowanie... --</option>';
            gminaSelect.disabled = true;

            if (!powiat) {
                gminaSelect.innerHTML = '<option value="">-- Najpierw wybierz powiat --</option>';
                return;
            }

            // Pobierz gminy dla wybranego województwa i powiatu
            fetch(`/api/gminy/?wojewodztwo=${encodeURIComponent(wojewodztwo)}&powiat=${encodeURIComponent(powiat)}`)
                .then(response => response.json())
                .then(data => {
                    gminaSelect.innerHTML = '<option value="">-- Wybierz gminę --</option>';
                    data.gminy.forEach(gmina => {
                        const option = document.createElement('option');
                        option.value = gmina.id;
                        option.textContent = `${gmina.nazwa} (${gmina.rodzaj})`;
                        gminaSelect.appendChild(option);
                    });
                    gminaSelect.disabled = false;
                })
                .catch(error => {
                    console.error('Błąd pobierania gmin:', error);
                    gminaSelect.innerHTML = '<option value="">-- Błąd ładowania --</option>';
                });
        });
    }

    // Walidacja formularza przed wysłaniem
    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const errors = [];

            // Sprawdź województwo
            if (!wojewodztwoSelect.value) {
                errors.push('Wybierz województwo');
                isValid = false;
            }

            // Sprawdź powiat
            if (!powiatSelect.value) {
                errors.push('Wybierz powiat');
                isValid = false;
            }

            // Sprawdź gminę
            if (!gminaSelect.value) {
                errors.push('Wybierz gminę');
                isValid = false;
            }

            // Sprawdź wielkość firmy
            const wielkoscFirmy = document.getElementById('id_wielkosc_firmy');
            if (wielkoscFirmy && !wielkoscFirmy.value) {
                errors.push('Wybierz wielkość firmy');
                isValid = false;
            }

            // Sprawdź wartość inwestycji
            const wartoscInwestycji = document.getElementById('id_wartosc_inwestycji');
            if (wartoscInwestycji) {
                const wartosc = parseFloat(wartoscInwestycji.value);
                if (isNaN(wartosc) || wartosc <= 0) {
                    errors.push('Podaj prawidłową wartość inwestycji');
                    isValid = false;
                }
            }

            // Jeśli formularz jest nieprawidłowy, pokaż błędy
            if (!isValid) {
                e.preventDefault();
                alert('Proszę poprawić następujące błędy:\n\n' + errors.join('\n'));
            }
        });
    }

    // Formatowanie liczb w wyniku (dodaj spacje co 3 cyfry)
    const formatNumbers = () => {
        const numberElements = document.querySelectorAll('.wynik-value, .wynik-highlight-value');
        numberElements.forEach(element => {
            const text = element.textContent;
            // Sprawdź czy to liczba z PLN
            if (text.includes('PLN')) {
                const number = text.replace(/[^\d.,]/g, '');
                if (number) {
                    const formatted = parseFloat(number.replace(',', '').replace('.', '')).toLocaleString('pl-PL', {
                        minimumFractionDigits: 0,
                        maximumFractionDigits: 0
                    });
                    element.textContent = formatted + ' PLN';
                }
            }
        });
    };

    // Uruchom formatowanie po załadowaniu strony
    formatNumbers();

    // Obsługa przycisku powrotu do góry (jeśli są wyniki)
    if (wynikiContainer) {
        const scrollToFormButton = document.createElement('button');
        scrollToFormButton.textContent = '↑ Wróć do formularza';
        scrollToFormButton.className = 'btn-secondary';
        scrollToFormButton.style.cssText = 'position: fixed; bottom: 20px; right: 20px; z-index: 1000; display: none;';
        scrollToFormButton.onclick = () => {
            form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        };
        document.body.appendChild(scrollToFormButton);

        // Pokaż przycisk gdy użytkownik przewinie poniżej formularza
        window.addEventListener('scroll', () => {
            const formRect = form.getBoundingClientRect();
            if (formRect.bottom < 0) {
                scrollToFormButton.style.display = 'block';
            } else {
                scrollToFormButton.style.display = 'none';
            }
        });
    }

    // Debug info w konsoli
    console.log('Kalkulator PSI załadowany');
    if (wojewodztwoSelect && powiatSelect && gminaSelect) {
        console.log('Elementy formularza znalezione:', {
            wojewodztwo: wojewodztwoSelect.value,
            powiat: powiatSelect.value,
            gmina: gminaSelect.value
        });
    }
});
