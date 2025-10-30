from django.contrib import admin

from .models import Gmina


@admin.register(Gmina)
class GminaAdmin(admin.ModelAdmin):
    list_display = [
        'nazwa',
        'rodzaj',
        'powiat',
        'wojewodztwo',
        'kod_teryt',
        'intensywnosc_pomocy',
        'minimalne_naklady',
        'gmina_tracaca',
    ]
    list_filter = [
        'wojewodztwo',
        'rodzaj',
        'intensywnosc_pomocy',
        'gmina_tracaca',
    ]
    search_fields = [
        'nazwa',
        'kod_teryt',
        'powiat',
        'wojewodztwo',
    ]
    readonly_fields = ['data_dodania', 'data_aktualizacji']
    ordering = ['wojewodztwo', 'powiat', 'nazwa']
    
    fieldsets = (
        ('Identyfikacja', {
            'fields': ('kod_teryt', 'nazwa', 'rodzaj', 'powiat', 'wojewodztwo')
        }),
        ('Parametry PSI', {
            'fields': ('intensywnosc_pomocy', 'minimalne_naklady', 'gmina_tracaca')
        }),
        ('Metadane', {
            'fields': ('data_dodania', 'data_aktualizacji'),
            'classes': ('collapse',)
        }),
    )
