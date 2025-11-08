from django.db import models


class Gmina(models.Model):
    """Model reprezentujący gminę w bazie danych PSI"""

    # Wybory rodzaju gminy
    RODZAJ_CHOICES = [
        ("GW", "Gmina wiejska"),
        ("GM", "Gmina miejska"),
        ("GMW", "Gmina miejsko-wiejska"),
        ("MNP", "Miasto na prawach powiatu"),
    ]

    # Identyfikacja
    kod_teryt = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Kod TERYT",
        help_text="Unikalny kod terytorialny gminy",
    )
    nazwa = models.CharField(max_length=100, verbose_name="Nazwa gminy")
    rodzaj = models.CharField(
        max_length=3,
        choices=RODZAJ_CHOICES,
        default="GMW",
        verbose_name="Rodzaj gminy",
        help_text="GW - wiejska, GM - miejska, GMW - miejsko-wiejska, MNP - miasto na prawach powiatu",
    )
    powiat = models.CharField(max_length=100, verbose_name="Powiat")
    wojewodztwo = models.CharField(max_length=50, verbose_name="Województwo")
    strefa_ekonomiczna = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Specjalna Strefa Ekonomiczna",
        help_text="Nazwa SSE zarządzającej tym obszarem",
    )

    # Parametry PSI
    intensywnosc_pomocy = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Intensywność pomocy (%)",
        help_text="Maksymalny procent kosztów kwalifikowanych (np. 50.00)",
    )
    minimalne_naklady = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Minimalne nakłady (PLN)",
        help_text="Minimalne nakłady inwestycyjne w złotych",
    )

    # Status gminy
    gmina_tracaca = models.BooleanField(
        default=False,
        verbose_name="Gmina tracąca funkcje",
        help_text="Czy gmina traci funkcje społeczno-gospodarcze",
    )

    # Metadane
    data_aktualizacji = models.DateTimeField(
        auto_now=True, verbose_name="Data aktualizacji"
    )
    data_dodania = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")

    class Meta:
        verbose_name = "Gmina"
        verbose_name_plural = "Gminy"
        ordering = ["wojewodztwo", "powiat", "nazwa"]
        indexes = [
            models.Index(fields=["kod_teryt"]),
            models.Index(fields=["wojewodztwo"]),
            models.Index(fields=["intensywnosc_pomocy"]),
        ]

    def __str__(self):
        return f"{self.nazwa} ({self.powiat}, {self.wojewodztwo})"

    def get_intensywnosc_display(self):
        """Zwraca intensywność pomocy jako procent"""
        return f"{self.intensywnosc_pomocy}%"

    def get_minimalne_naklady_display(self):
        """Zwraca minimalne nakłady w formacie czytelnym"""
        if self.minimalne_naklady is None:
            return "-"
        return f"{self.minimalne_naklady:,.2f} PLN".replace(",", " ")
