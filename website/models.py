from django.db import models
from tinymce.models import HTMLField


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

    def get_liczba_kryteriow_jakosciowych(self):
        """Zwraca liczbę kryteriów jakościowych do spełnienia na podstawie intensywności"""
        intensywnosc = float(self.intensywnosc_pomocy)

        if intensywnosc >= 50:
            return 4
        elif intensywnosc >= 40:
            return 5
        else:
            return 6


class Artykul(models.Model):
    """Model artykułu blogowego o PSI"""

    tytul = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.SlugField(
        max_length=200, unique=True, verbose_name="URL (slug)", blank=True
    )
    lead = models.TextField(verbose_name="Krótki opis (lead)", max_length=300)
    tresc = HTMLField(verbose_name="Treść artykułu")

    # Metadata
    data_publikacji = models.DateTimeField(
        auto_now_add=True, verbose_name="Data publikacji"
    )
    data_aktualizacji = models.DateTimeField(
        auto_now=True, verbose_name="Data aktualizacji"
    )
    opublikowany = models.BooleanField(default=True, verbose_name="Opublikowany")

    class Meta:
        verbose_name = "Artykuł"
        verbose_name_plural = "Artykuły"
        ordering = ["-data_publikacji"]

    def __str__(self):
        return self.tytul

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify

            self.slug = slugify(self.tytul)
        super().save(*args, **kwargs)
