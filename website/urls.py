from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gminy/', views.gminy_list, name='gminy_list'),
]
