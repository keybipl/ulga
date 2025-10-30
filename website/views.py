from django.shortcuts import render

from .models import Gmina

# Create your views here.


def home(request):
    return render(request, 'website/base.html')


def gminy_list(request):
    """Widok z listą wszystkich gmin z województwami, powiatami i intensywnością pomocy"""
    # Pobierz wszystkie gminy uporządkowane po województwie, powiecie i nazwie
    gminy = Gmina.objects.all().order_by('wojewodztwo', 'powiat', 'nazwa')
    
    # Zlicz gminy według województw
    wojewodztwa_stats = {}
    for gmina in gminy:
        if gmina.wojewodztwo not in wojewodztwa_stats:
            wojewodztwa_stats[gmina.wojewodztwo] = {
                'count': 0,
                'intensywnosc': {}
            }
        wojewodztwa_stats[gmina.wojewodztwo]['count'] += 1
        
        # Zlicz według intensywności
        intensywnosc = float(gmina.intensywnosc_pomocy)
        if intensywnosc not in wojewodztwa_stats[gmina.wojewodztwo]['intensywnosc']:
            wojewodztwa_stats[gmina.wojewodztwo]['intensywnosc'][intensywnosc] = 0
        wojewodztwa_stats[gmina.wojewodztwo]['intensywnosc'][intensywnosc] += 1
    
    context = {
        'gminy': gminy,
        'wojewodztwa_stats': wojewodztwa_stats,
        'total_count': gminy.count(),
    }
    
    return render(request, 'website/gminy_list.html', context)
    return render(request, 'website/gminy_list.html', context)
