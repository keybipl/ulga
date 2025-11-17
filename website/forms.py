"""
Formularze Django dla aplikacji website.
"""
from django import forms
from .models import Gmina


class KalkulatorPSIForm(forms.Form):
    """
    Formularz kalkulatora PSI (Polska Strefa Inwestycji).
    """

    # Kaskadowe wybory: Województwo → Powiat → Gmina
    wojewodztwo = forms.ChoiceField(
        label='Województwo',
        choices=[('', '--- Wybierz województwo ---')],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_wojewodztwo'
        })
    )

    powiat = forms.ChoiceField(
        label='Powiat',
        choices=[('', '--- Najpierw wybierz województwo ---')],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_powiat',
            'disabled': True
        })
    )

    gmina = forms.ModelChoiceField(
        label='Gmina',
        queryset=Gmina.objects.none(),
        required=True,
        empty_label='--- Najpierw wybierz powiat ---',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_gmina',
            'disabled': True
        })
    )

    wielkosc_firmy = forms.ChoiceField(
        label='Wielkość firmy',
        choices=[
            ('', '--- Wybierz wielkość ---'),
            ('mikro', 'Mikroprzedsiębiorstwo'),
            ('mala', 'Małe przedsiębiorstwo'),
            ('srednia', 'Średnie przedsiębiorstwo'),
            ('duza', 'Duże przedsiębiorstwo'),
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_wielkosc_firmy'
        })
    )

    nowy_zaklad = forms.ChoiceField(
        label='Rodzaj zakładu',
        choices=[
            ('True', 'Nowy zakład'),
            ('False', 'Istniejący zakład'),
        ],
        required=True,
        initial='True',
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        })
    )

    wartosc_inwestycji = forms.DecimalField(
        label='Wartość inwestycji (PLN)',
        min_value=0,
        max_digits=15,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'np. 5000000',
            'step': '0.01'
        }),
        help_text='Podaj planowaną wartość inwestycji w złotych'
    )

    tylko_bpo = forms.BooleanField(
        label='Działalność prowadzona TYLKO w sektorze BPO',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'id_tylko_bpo'
        }),
        help_text='Zaznacz, jeśli w ramach projektu inwestycyjnego będziesz prowadzić wyłącznie działalność w sektorze nowoczesnych usług dla biznesu (BPO). To obniża minimalne nakłady do poziomu małej firmy.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Wypełnij wybory województw z bazy danych
        wojewodztwa = Gmina.objects.values_list('wojewodztwo', flat=True).distinct().order_by('wojewodztwo')
        self.fields['wojewodztwo'].choices = [('', '--- Wybierz województwo ---')] + \
                                              [(w, w) for w in wojewodztwa]

        # Jeśli formularz jest wypełniony (POST), ustaw odpowiednie querysety
        if self.data:
            try:
                wojewodztwo = self.data.get('wojewodztwo')
                if wojewodztwo:
                    powiaty = Gmina.objects.filter(
                        wojewodztwo=wojewodztwo
                    ).values_list('powiat', flat=True).distinct().order_by('powiat')
                    self.fields['powiat'].choices = [('', '--- Wybierz powiat ---')] + \
                                                     [(p, p) for p in powiaty]
                    self.fields['powiat'].widget.attrs.pop('disabled', None)

                powiat = self.data.get('powiat')
                if wojewodztwo and powiat:
                    self.fields['gmina'].queryset = Gmina.objects.filter(
                        wojewodztwo=wojewodztwo,
                        powiat=powiat
                    ).order_by('nazwa')
                    self.fields['gmina'].widget.attrs.pop('disabled', None)

            except (ValueError, TypeError):
                pass

    def clean_nowy_zaklad(self):
        """Konwertuje string na boolean."""
        value = self.cleaned_data.get('nowy_zaklad')
        return value == 'True'
